import unittest

from chainer import testing
import numpy as np

from chainerrl.links import empirical_normalization


class TestEmpiricalNormalization(unittest.TestCase):
    def test_small(self):
        en = empirical_normalization.EmpiricalNormalization(10)
        xs = []
        for t in range(10):
            x = np.random.normal(loc=4, scale=2, size=(t+3, 10))
            en(x)
            xs.extend(list(x))
        xs = np.array(xs)
        true_mean = np.mean(xs, axis=0, keepdims=True)
        true_std = np.std(xs, axis=0, keepdims=True)
        np.testing.assert_allclose(en.mean, true_mean, rtol=1e-4)
        np.testing.assert_allclose(np.sqrt(en.var), true_std, rtol=1e-4)

    @testing.attr.slow
    def test_large(self):
        en = empirical_normalization.EmpiricalNormalization(10)
        for _ in range(10000):
            x = np.random.normal(loc=4, scale=2, size=(7, 10))
            en(x)
        x = 2 * np.random.normal(loc=4, scale=2, size=(1, 10))
        enx = en(x, update=False)
        # mean, std = en.mean_and_std()
        mean = en.mean
        std = np.sqrt(en.var)
        np.testing.assert_allclose(mean, np.full_like(mean, 4), rtol=1e-1)
        np.testing.assert_allclose(std, np.full_like(std, 2), rtol=1e-1)

        # Compare with the ground-truth normalization
        np.testing.assert_allclose((x - 4) / 2, enx, rtol=1e-1)

        # Test inverse
        np.testing.assert_allclose(x, en.inverse(enx), rtol=1e-4)
