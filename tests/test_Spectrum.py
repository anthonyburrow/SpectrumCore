import numpy as np
import pytest

from SpectrumCore import Spectrum


def test_initialization(simple_data):
    spec = Spectrum(simple_data)
    assert spec is not None


def test_empty_initialization():
    with pytest.raises(TypeError):
        Spectrum()


def test_slicing(simple_data, spectrum):
    assert np.all(spectrum[1:3].data == simple_data[1:3])


def test_length(simple_data, spectrum):
    assert len(spectrum) == len(simple_data)


def test_properties(simple_data_error, spectrum_error):
    assert spectrum_error.wave_start == simple_data_error[0, 0]
    assert spectrum_error.wave_end == simple_data_error[-1, 0]
    assert np.all(spectrum_error.wave == simple_data_error[:, 0])
    assert np.all(spectrum_error.flux == simple_data_error[:, 1])
    assert np.all(spectrum_error.error == simple_data_error[:, 2])


def test_normalize_flux(spectrum):
    spectrum.normalize_flux()
    assert spectrum.flux.max() == 1.


def test_normalize_wave(spectrum):
    spectrum.normalize_wave()
    assert spectrum.wave_start == 0.
    assert spectrum.wave_end == 1.


def test_add_flux(spectrum):
    old_flux = spectrum.flux.copy()
    added_flux = np.ones(len(spectrum))
    spectrum.add_flux(added_flux)

    assert np.all(spectrum.flux == old_flux + added_flux)
