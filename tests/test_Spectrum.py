import numpy as np

from SpectrumCore import Spectrum


def test_instantiate():
    data = np.array([
        [5000., 0.4],
        [5100., 0.6],
        [5200., 0.5],
        [5300., 0.4],
        [5400., 0.3],
    ])

    spec = Spectrum(data)
    # spec.normalize()
    print(spec)
