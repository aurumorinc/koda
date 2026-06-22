import sys
import os
import importlib.util

from unittest.mock import MagicMock

def import_script(relative_path: str, module_name: str):
    """
    Dynamically imports a script from apps/koda-api/f/.
    """
    if "wmill" not in sys.modules:
        sys.modules["wmill"] = MagicMock()
        
    tests_dir = os.path.dirname(__file__)
    apps_koda_api_dir = os.path.dirname(tests_dir)
    script_path = os.path.abspath(os.path.join(apps_koda_api_dir, relative_path))
    
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load {script_path}")
        
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
