# -*- coding: utf-8 -*-

"""
The model classes and functions for microstructure (image) analysis.
"""

import numpy as np
import scipy.stats as stats
from numpy.typing import NDArray
from scipy import optimize

from microtex.quantities import R

__all__ = tuple(["FFT_Analyser_2D", "Domain_Analyser_2D"])


# 3-params Gaussian curve to fit peak
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-(((x - mean) / 4 / stddev) ** 2))


class FFT_Analyser_2D:
    """
    FFT power spectrum analysis tool

    see # https://bertvandenbroucke.netlify.app/2019/05/24/computing-a-power-spectrum-in-python/
    """

    def __init__(self, configuration) -> None:
        """Create FFT analyzer instance for square domains of size nx"""
        self.configuration = configuration
        # wave vectors
        kfreq = np.fft.fftfreq(self.configuration.nx) * self.configuration.nx
        # to a pixel frequency
        kfreq2D = np.meshgrid(kfreq, kfreq)
        # norms of wave vectors
        knrm = np.sqrt(kfreq2D[0] ** 2 + kfreq2D[1] ** 2)
        # we need flatten layout
        self.knrm = knrm.flatten()
        # wave number bins
        self.kbins = np.arange(0.5, self.configuration.nx // 2 + 1, 1)
        # k values are the midpoints
        self.kvals = 0.5 * (self.kbins[1:] + self.kbins[:-1])

    def analyze_domain(self, domain: NDArray) -> None:
        fi = np.fft.fftn(domain - domain.mean())
        fa = np.abs(fi) ** 2
        self.Abins, _, _ = stats.binned_statistic(
            self.knrm, fa.flatten(), statistic="mean", bins=self.kbins
        )
        self.Abins *= np.pi * (self.kbins[1:] ** 2 - self.kbins[:-1] ** 2)

    def power_spectrum(self):
        return self.configuration.nx / self.kvals, self.Abins

    def fit_gaussian(self, **kwargs):
        gs = self.configuration.nx / self.kvals
        # set reasonable guess
        if "p0" not in kwargs:
            kwargs["p0"] = np.array([self.Abins.max(), gs[self.Abins.argmax()], 1])
        try:
            popt, pcov = optimize.curve_fit(gaussian, gs, self.Abins, **kwargs)
            perr = np.sqrt(np.diag(pcov))
        except (ValueError, RuntimeError):
            # alternative estimate
            popt = [np.nan, gs[np.argsort(self.Abins)[-10:]].mean(), 3 * gs[np.argsort(self.Abins)[-10:]].std()]
            perr = np.inf
        return popt, perr


class Domain_Analyser_2D:
    """
    Domain related post-processing analyses

    """

    def __init__(self, configuration) -> None:
        self.configuration = configuration

    def calculate_energy(self, domain: NDArray) -> float:
        """Returns integral value of total diffusion potential over domain"""
        # Chemical diffusion potential term
        mu_chem = R * self.configuration.T * (np.log(domain) - np.log(1.0 - domain)) + self.configuration.omega * (1.0 - 2.0 * domain)

        # Gradient diffusion potential term
        c_e, c_w = np.roll(domain, -1, axis=1), np.roll(domain, 1, axis=1)
        c_s, c_n = np.roll(domain, -1, axis=0), np.roll(domain, 1, axis=0)

        mu_grad_x = (c_e - 2.0 * domain + c_w) / self.configuration.dx / self.configuration.dx
        mu_grad_y = (c_n - 2.0 * domain + c_s) / self.configuration.dy / self.configuration.dy
        mu_grad = -self.configuration.kappa * (mu_grad_x + mu_grad_y)

        # Total diffusion potential
        mu = mu_chem + mu_grad
        return np.mean(np.abs(mu))
