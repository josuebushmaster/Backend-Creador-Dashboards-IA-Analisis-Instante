import importlib
import sys
from pathlib import Path

# Añadir la raíz del proyecto al sys.path para que 'src' sea importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    m = importlib.import_module('src.presentation.api.routes.charts')
    print('IMPORT OK')
except Exception as e:
    print('IMPORT ERROR')
    import traceback
    traceback.print_exc()