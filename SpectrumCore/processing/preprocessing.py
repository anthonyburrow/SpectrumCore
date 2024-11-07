import numpy as np

from ..physics.doppler import deredshift
from ..physics.deredden import deredden
from ..physics.telluric import remove_telluric
# from ..physics.mangle import mangle


def preprocess(*args, **kwargs) -> np.ndarray:
    data = remove_nans(*args, **kwargs)
    data = remove_nonpositive(*args, **kwargs)

    # TODO: Do after mangling
    data = remove_telluric(*args, **kwargs)
    data = deredshift(*args, **kwargs)
    data = prune(*args, **kwargs)
    # TODO: Mangle
    # data = mangle(*args, **kwargs)
    data = deredden(*args, **kwargs)

    data = normalize(*args, **kwargs)

    return data


def remove_nans(
    data: np.ndarray, remove_nans: bool = True, *args, **kwargs
) -> np.ndarray:
    """Remove NaN values."""
    if not remove_nans:
        return data

    nan_mask = ~np.isnan(data).any(axis=1)
    return data[nan_mask]


def remove_nonpositive(
    data: np.ndarray, remove_nonpositive=True, *args, **kwargs
) -> np.ndarray:
    """Remove non-positive values."""
    if not remove_nonpositive:
        return data

    mask = data[:, 1] > 0.
    return data[mask]


def prune(
    data: np.ndarray, wave_range: tuple[float] = None, *args, **kwargs
) -> np.ndarray:
    if wave_range is None:
        return data

    mask = (wave_range[0] <= data[:, 0]) & (data[:, 0] <= wave_range[1])
    return data[mask]


def normalize(
    data: np.ndarray, normalize: bool = False, norm_method: str = None,
    *args, **kwargs
) -> np.ndarray:
    if not normalize:
        return data

    if norm_method is None or norm_method == 'max':
        norm = data[:, 1].max()
    elif norm_method == 'mean':
        norm = data[:, 1].mean()
    else:
        print('Spectrum was not normalized.')

    data[:, 1] /= norm
    try:
        data[:, 2] /= norm
    except IndexError:
        pass

    return data
