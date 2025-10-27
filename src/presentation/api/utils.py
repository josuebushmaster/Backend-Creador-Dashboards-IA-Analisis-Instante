
"""
Utilities para presentación: sanitización de objetos antes de serializar a JSON.

Convierte valores no finitos (NaN, Inf) a None y normaliza tipos de numpy/pandas
a tipos nativos de Python para evitar errores de serialización JSON.
"""
from typing import Any
import math
import numbers

try:
    import numpy as np
except Exception:
    np = None

try:
    import pandas as pd
except Exception:
    pd = None


def sanitize_for_json(value: Any) -> Any:
    """Recorre recursivamente diccionarios/listas y convierte valores no serializables:

    - np.nan / float('nan') -> None
    - inf / -inf -> None
    - numpy/pandas scalar types -> valor nativo (item())
    - pandas NA/NaT -> None

    Mantiene otros tipos intactos.
    """
    # None stays None
    if value is None:
        return None

    # pandas NA, NaT, numpy.nan
    try:
        if pd is not None and pd.isna(value):
            return None
    except Exception:
        # pd.isna puede lanzar para tipos extraños; ignoramos
        pass

    # numpy scalar -> native
    try:
        if np is not None and isinstance(value, np.generic):
            native = value.item()
            return sanitize_for_json(native)
    except Exception:
        pass

    # numbers: handle floats (check finite) and other numbers
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return value

    if isinstance(value, numbers.Number) and not isinstance(value, bool):
        # ints are safe
        return value

    # dict-like
    if isinstance(value, dict):
        return {k: sanitize_for_json(v) for k, v in value.items()}

    # list/tuple/set -> list
    if isinstance(value, (list, tuple, set)):
        return [sanitize_for_json(v) for v in value]

    # fallback: try to convert numpy arrays and pandas structures
    try:
        if np is not None and isinstance(value, (np.ndarray,)):
            return [sanitize_for_json(v) for v in value.tolist()]
    except Exception:
        pass

    # final fallback: return as-is
    return value
