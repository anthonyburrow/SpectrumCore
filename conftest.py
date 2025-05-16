import pytest
import numpy as np

from SpectrumCore import Spectrum


@pytest.fixture
def simple_data():
    data = np.array([
        [5000., 0.4],
        [5100., 0.6],
        [5200., 0.5],
        [5300., 0.4],
        [5400., 0.3],
    ])

    return data


@pytest.fixture
def simple_data_error():
    data = np.array([
        [5000., 0.4, 0.004],
        [5100., 0.6, 0.006],
        [5200., 0.5, 0.005],
        [5300., 0.4, 0.004],
        [5400., 0.3, 0.003],
    ])

    return data


@pytest.fixture
def spectrum(simple_data):
    return Spectrum(simple_data)


@pytest.fixture
def spectrum_error(simple_data_error):
    return Spectrum(simple_data_error)
