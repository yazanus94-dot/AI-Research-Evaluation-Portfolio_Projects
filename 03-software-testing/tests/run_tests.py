"""Minimal runner for environments without pytest: python tests/run_tests.py"""
import importlib.util, inspect, pathlib, sys, tempfile, traceback
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent))
fails = n = 0
for f in sorted(here.glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for name, fn in inspect.getmembers(m, inspect.isfunction):
        if not name.startswith("test_"): continue
        n += 1
        try:
            fn(*([pathlib.Path(tempfile.mkdtemp())] if "tmp_path" in inspect.signature(fn).parameters else []))
        except Exception:
            fails += 1; print("FAIL", f.name, name); traceback.print_exc()
print(f"{n - fails}/{n} passed"); sys.exit(1 if fails else 0)
