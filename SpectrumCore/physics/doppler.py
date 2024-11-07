import numpy as np


def deredshift(
    data: np.ndarray,
    z: float = None,
    *args, **kwargs
) -> np.ndarray:
    """De-redshift wavelength values."""
    if z is None:
        return data

    data[:, 0] /= (z + 1.)

    return data
