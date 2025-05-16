import numpy as np

from .io import read
from .util.interpolate import interp_linear
from .physics.telluric import telluric_features
from .physics.deredden import deredden_ccm


class Spectrum:

    def __init__(self, data: np.ndarray | str):
        if isinstance(data, str):
            self.data = read(data)
        else:
            self.data = data

        self.has_error = self.data.shape[1] == 3

        self._flux_norm = 1.
        self._orig_wave_scale = None

    def normalize_flux(self, method: str = None, wave_range: tuple[float] = None):
        if wave_range is None:
            flux = self.flux
        else:
            if self._orig_wave_scale is not None:
                self._orig_wave_scale
            flux = self.flux[self.mask_between(wave_range)]

        if method is None or method == 'max':
            norm = flux.max()
        elif method == 'mean':
            norm = flux.mean()
        else:
            print('Spectrum was not normalized.')

        self._flux_norm *= norm

        self.data[:, 1] /= norm
        if self.has_error:
            self.data[:, 2] /= norm

    def normalize_wave(self, wave_range: tuple[float] = None):
        if wave_range is None:
            self._orig_wave_scale = self.wave_start, self.wave_end
        else:
            self._orig_wave_scale = wave_range

        min_wave, max_wave = self._orig_wave_scale
        self.data[:, 0] = (self.wave - min_wave) / (max_wave - min_wave)

    def downsample(self, factor):
        n_bins = int(len(self.data) / factor)

        n_cols = 3 if self.has_error else 2
        data_ends = np.zeros((n_bins + 1, n_cols))

        data_ends[:, 0], bin_size = \
            np.linspace(self.wave_start, self.wave_end, n_bins + 1, retstep=True)

        data_DS = np.zeros((n_bins, n_cols))
        data_DS[:, 0] = 0.5 * (data_ends[:-1, 0] + data_ends[1:, 0])

        if self.has_error:
            data_ends[:, 1], data_ends[:, 2] = \
                interp_linear(data_ends[:, 0], self.data)
        else:
            data_ends[:, 1] = interp_linear(data_ends[:, 0], self.data)

        for i in range(n_bins):
            # Get bin values (endpoints + data between endpoints)
            mask_bin = self.mask_between((data_ends[i, 0], data_ends[i + 1, 0]))
            data_bin = np.zeros((mask_bin.sum() + 2, n_cols))

            data_bin[[0, -1]] = data_ends[i:i + 2]
            data_bin[1:-1] = self.data[mask_bin]
            if self.has_error:
                data_bin[:, 2] **= 2.

            # Get flux/flux error associated with integrated flux
            bin_wave = data_bin[:, 0]
            bin_flux = data_bin[:, 1]

            dlam = bin_wave[1:] - bin_wave[:-1]
            lamF = bin_wave * bin_flux

            flux_terms = dlam * (lamF[:-1] + lamF[1:])
            data_DS[i, 1] = 0.5 * flux_terms.sum()

            if self.has_error:
                bin_flux_var = data_bin[:, 2]
                lamF_var = bin_wave**2 * bin_flux_var

                var_terms = dlam**2 * (lamF_var[:-1] + lamF_var[1:])
                data_DS[i, 2] = 0.25 * var_terms.sum()

        lam_dlam = data_DS[:, 0] * bin_size
        data_DS[:, 1] /= lam_dlam
        if self.has_error:
            data_DS[:, 2] = np.sqrt(data_DS[:, 2]) / lam_dlam

        self.data = data_DS

    def add_flux(self, flux):
        self.data[:, 1] += flux

    def prune(self, wave_range: tuple[float]):
        self.data = self.between(wave_range)

    def between(self, wave_range: tuple[float]) -> np.ndarray:
        return self.data[self.mask_between(wave_range)]

    def mask_between(self, wave_range: tuple[float]) -> np.ndarray:
        mask = (wave_range[0] <= self.wave) & (self.wave <= wave_range[1])
        return mask

    def remove_nans(self):
        nan_mask = ~np.isnan(self.data).any(axis=1)
        self.data = self.data[nan_mask]

    def remove_nonpositive(self):
        mask = self.flux > 0.
        self.data = self.data[mask]

    def remove_telluric(self):
        for feature in telluric_features:
            min_ind, max_ind = np.searchsorted(self.wave, feature)
            if min_ind == max_ind:
                # Feature completely outside wavelengths, ignore it
                continue
            if min_ind == 0 or max_ind == len(self.wave):
                # Spectrum begins/ends inside telluric,
                # remove instead since no line can be made
                telluric_mask = self.mask_between(feature)
                self.data = self.data[~telluric_mask]
                continue

            telluric_inds = np.arange(min_ind, max_ind)

            min_ind -= 1
            slope = (self.flux[max_ind] - self.flux[min_ind]) / (self.wave[max_ind] - self.wave[min_ind])
            self.data[telluric_inds, 1] = slope * (self.wave[telluric_inds] - self.wave[min_ind]) + self.flux[min_ind]

    def deredshift(self, z: float = 0.):
        self.data[:, 0] /= (z + 1.)

    def deredden(
        self, E_BV: float = None, R_V: float = None,
        *args, **kwargs
    ):
        self.data[:, 1] = deredden_ccm(self.data, E_BV=E_BV, R_V=R_V)

    @property
    def wave(self):
        return self.data[:, 0]

    @property
    def wave_start(self):
        return self.data[0, 0]

    @property
    def wave_end(self):
        return self.data[-1, 0]

    @property
    def flux(self):
        return self.data[:, 1]

    @property
    def error(self):
        if self.has_error:
            return self.data[:, 2]
        return None

    def __getitem__(self, key):
        return Spectrum(self.data[key])

    def __array__(self, dtype=None):
        return np.asarray(self.data, dtype=dtype)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)
