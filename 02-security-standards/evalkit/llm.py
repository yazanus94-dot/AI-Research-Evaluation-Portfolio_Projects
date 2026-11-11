"""Model adapters. `mock-oracle` and `mock-trap` exist ONLY to test the harness (they are not real models).

  mock-oracle            always returns the answer key         -> harness must report 100% pass
  mock-trap              always returns the documented shortcut -> harness must report 0% pass
  openai:<model>         needs OPENAI_API_KEY   (pip install openai)
  anthropic:<model>      needs ANTHROPIC_API_KEY (pip install anthropic)
  ollama:<model>         local models via OLLAMA_HOST (default http://localhost:11434)
"""
from __future__ import annotations

import os

from evalkit.grader import fmt_answer
from evalkit.schema import Question

SYSTEM = ("You are an expert taking a rigorous exam. Work through the problem carefully, check the exact wording and any stated "
          "conventions, then finish with ONE final line in the form 'FINAL ANSWER: <answer only>'. "
          "Give the answer in the requested units/precision; do not add explanations after that line.")


class MockOracle:
    name = "mock-oracle"

    def respond(self, q: Question) -> str:
        return f"(oracle)\nFINAL ANSWER: {fmt_answer(q.answer)}"


class MockTrap:
    name = "mock-trap"

    def respond(self, q: Question) -> str:
        return f"(falls for the shortcut)\nFINAL ANSWER: {fmt_answer(q.naive_answer)}"


class OpenAIModel:
    def __init__(self, model: str):
        from openai import OpenAI
        self.client, self.model, self.name = OpenAI(), model, f"openai:{model}"

    def respond(self, q: Question) -> str:
        r = self.client.chat.completions.create(model=self.model, temperature=0,
                                                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": q.question}])
        return r.choices[0].message.content or ""


class AnthropicModel:
    def __init__(self, model: str):
        import anthropic
        self.client, self.model, self.name = anthropic.Anthropic(), model, f"anthropic:{model}"

    def respond(self, q: Question) -> str:
        r = self.client.messages.create(model=self.model, max_tokens=2000, temperature=0, system=SYSTEM,
                                        messages=[{"role": "user", "content": q.question}])
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


class OllamaModel:
    def __init__(self, model: str):
        self.host, self.model, self.name = os.getenv("OLLAMA_HOST", "http://localhost:11434"), model, f"ollama:{model}"

    def respond(self, q: Question) -> str:
        import requests
        r = requests.post(f"{self.host}/api/chat", timeout=300, json={
            "model": self.model, "stream": False, "options": {"temperature": 0},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": q.question}]})
        r.raise_for_status()
        return r.json()["message"]["content"]


def get_model(spec: str):
    if spec == "mock-oracle":
        return MockOracle()
    if spec == "mock-trap":
        return MockTrap()
    kind, _, model = spec.partition(":")
    table = {"openai": OpenAIModel, "anthropic": AnthropicModel, "ollama": OllamaModel}
    if kind not in table or not model:
        raise ValueError("model spec must be mock-oracle | mock-trap | openai:<model> | anthropic:<model> | ollama:<model>")
    return table[kind](model)
