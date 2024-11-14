import numpy as np


def smooth_boxcar(data, smooth_window=10, *args, **kwargs):
    box = np.ones(smooth_window) / float(smooth_window)
    data[:, 1] = np.convolve(data[:, 1], box, mode='same')

    return data


def smooth(data, smooth_method=None, *args, **kwargs):
    if smooth_method is None:
        return data

    if smooth_method == 'boxcar':
        return smooth_boxcar(data, *args, **kwargs)
    elif smooth_method == 'sg':
        pass
