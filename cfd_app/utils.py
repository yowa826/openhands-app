# utils.py - Utility functions

import numpy as np
from pathlib import Path
import os

def arrays_to_csv(u: np.ndarray, v: np.ndarray, p: np.ndarray, fname: str) -> Path:
    """Save u, v, p arrays to a CSV file."""
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    data = np.column_stack((u.flatten(), v.flatten(), p.flatten()))
    header = 'u,v,p'
    np.savetxt(fname, data, delimiter=',', header=header, comments='')
    return Path(fname)
