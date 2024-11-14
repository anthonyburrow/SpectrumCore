import numpy as np
from scipy.signal import savgol_filter


def smooth_boxcar(data, smooth_window=10, *args, **kwargs):
    box = np.ones(smooth_window) / float(smooth_window)
    data[:, 1] = np.convolve(data[:, 1], box, mode='same')

    return data


def smooth_sg(data, smooth_window=10, *args, **kwargs):
    order = 3
    data[:, 1] = savgol_filter(
        data[:, 1], window_length=smooth_window, polyorder=order
    )

    return data


def smooth(data, smooth_method=None, *args, **kwargs):
    if smooth_method is None:
        return data

    if smooth_method == 'boxcar':
        return smooth_boxcar(data, *args, **kwargs)
    elif smooth_method == 'sg':
        return smooth_sg(data, *args, **kwargs)
