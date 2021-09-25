# -*- coding: utf-8 -*-


"""
See the :code:`modeling.__ini__.py` module.
"""


from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from microtex.quantities import R


__all__ = tuple(["Cahn_Hilliard_2D_AB_Solver", "Configuration"])


@dataclass(frozen=True)
class Configuration:
    T: float = 600             # Temperature
    nx: float = 2 ** 8         # Number of grid along x direction
    ny: float = 2 ** 8         # Number of grid along x direction
    dx: float = 2.0e-9         # Spacing of grids in x direction [m]
    dy: float = 2.0e-9         # Spacing of grids in y direction [m]
    dt: float = 60             # Time increment [s]
    c0: float = 0.6            # Average composition of B atom [atomic fraction]
    kappa: float = 3.0e-14     # Gradient coefficient [Jm2/mol]
    omega: float = 16000.0     # Atom intaraction constant [J/mol]
    Qa: float = 240000.0
    Aa: float = 1.0
    Qb: float = 240000.0
    Ab: float = 1.0

    @property
    def Da(self) -> float:
        """
        Diffusion coefficient of A atom [m2/s].
        """
        return self.Aa * np.exp(-self.Qa / R / self.T)

    @property
    def Db(self) -> float:
        """
        Diffusion coefficient of B atom [m2/s].
        """
        return self.Ab * np.exp(-self.Qb / R / self.T)

    @property
    def D(self) -> Tuple:
        return self.Da, self.Db

    @classmethod
    def keys(self):
        return ['T', 'nx', 'ny', 'dx', 'dy', 'c0', 'kappa', 'omega', 'Da', 'Db', 'dt']

    def __getitem__(self, key):
        return getattr(self, key)

    def noisy_field(self, noise=0.01) -> NDArray:
        return self.c0 + np.random.rand(self.nx, self.ny) * noise - noise / 2


def _get_neighbours(c: NDArray) -> Tuple[NDArray, NDArray, NDArray, NDArray]:
    """Returns rolled arrays representing four neighbour values
    east(E), west (W), south (S) and north (N)
    """
    return (
        np.roll(c, -1, axis=1),
        np.roll(c, 1, axis=1),
        np.roll(c, -1, axis=0),
        np.roll(c, 1, axis=0),
    )


def Cahn_Hilliard_2D_AB_Solver(domain: NDArray, c: Configuration) -> NDArray:
    """
    Cahn-Hilliard 2D phase-field model solver with finite differences and periodic boundaries.

    The numpy vectorized version of Cahn-Hilliard solver.
    Update a conserved order parameter, in our case, the concetration field $c(\vb{x}, t)$.
    Calculate free energy derivative at domain nodes.
    The four neighbour nodes of the central node (C) are east(E), west (W),north (N)
    and south (S).

             N
             |
         W---C---E
             |
             S
    """
    # Chemical potential term.
    mu_chem = R * c.T * (np.log(domain) - np.log(1.0 - domain)) + c.omega * (1.0 - 2.0 * domain)

    # Gradient potential term.
    c_e, c_w, c_s, c_n = _get_neighbours(domain)
    mu_grad = -c.kappa * (
        (c_e - 2.0 * domain + c_w) / c.dx / c.dx + (c_n - 2.0 * domain + c_s) / c.dy / c.dy
    )

    # Total chemical potential.
    mu = mu_chem + mu_grad

    # Gradient of chemical potential
    mu_e, mu_w, mu_s, mu_n = _get_neighbours(mu)
    nabla_mu = (mu_w - 2.0 * mu + mu_e) / c.dx / c.dx + (mu_n - 2.0 * mu + mu_s) / c.dy / c.dy

    DbDa = c.Db / c.Da

    M = (c.Da / R / c.T) * (domain + DbDa * (1.0 - domain)) * domain * (1.0 - domain)

    dm_dc = (c.Da / R / c.T) * (
        (1.0 - DbDa) * domain * (1.0 - domain)
        + (domain + DbDa * (1.0 - domain)) * (1.0 - 2.0 * domain)
    )

    dc2_dx2 = ((c_e - c_w) * (mu_e - mu_w)) / (4.0 * c.dx * c.dx)
    dc2_dy2 = ((c_n - c_s) * (mu_n - mu_s)) / (4.0 * c.dy * c.dy)

    dc_dt = M * nabla_mu + dm_dc * (dc2_dx2 + dc2_dy2)

    return domain + dc_dt * c.dt


def Cahn_Hilliard_1D_AB_Solver_Naive(domain: NDArray, c: Configuration) -> NDArray:
    # Chemical potential term.
    # Gradient potential term.
    # Total chemical potential.
    # Gradient of chemical potential.
    return NotImplemented


def Cahn_Hilliard_2D_AB_Solver_Naive(domain: NDArray, c: Configuration) -> NDArray:
    # Chemical potential term.
    # Gradient potential term.
    # Total chemical potential.
    # Gradient of chemical potential.
    return NotImplemented