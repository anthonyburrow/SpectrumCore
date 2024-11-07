import numpy as np


telluric_to_remove = [
    (5876., 5940.),
    (6849., 6929.),
    (7576., 7688.),
]


def remove_telluric(data, remove_telluric=False, *args, **kwargs):
    """Remove telluric features before redshift correction."""
    if not remove_telluric:
        return data

    wave = data[:, 0]
    flux = data[:, 1]

    for feature in telluric_to_remove:
        min_ind, max_ind = np.searchsorted(wave, feature)
        if min_ind == max_ind:
            # Feature completely outside wavelengths, ignore it
            continue
        if min_ind == 0 or max_ind == len(wave):
            # Spectrum begins/ends inside telluric,
            # remove instead since no line can be made
            telluric_mask = (feature[0] <= wave) & (wave <= feature[1])
            data = data[~telluric_mask]
            continue

        telluric_inds = np.arange(min_ind, max_ind)

        min_ind -= 1
        slope = (flux[max_ind] - flux[min_ind]) / (wave[max_ind] - wave[min_ind])
        flux[telluric_inds] = slope * (wave[telluric_inds] - wave[min_ind]) + flux[min_ind]

    return data
