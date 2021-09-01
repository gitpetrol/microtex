# -*- coding: utf-8 -*-

"""
This module contains a model classes.
"""

from __future__ import annotations

from typing import Any, Callable

from numpy.typing import NDArray

from microtex.modeling import Model2D, Solver


class Cahn_Hilliard_2D_AB_Model(Model2D):
    """¨
    The Cahn-Hilliard 2D phase-field model for AB (binary) solid solution.


    # Using the model class wchi wraps the solver.

    model = Cahn_Hilliard_2D_AB_Model(
        dx=dx, dy=dy, dt=dt, R=R, La=La, T=T0, ac=ac, Da=Da, Db=Db,
        domain=fields[-1], solver=Cahn_Hilliard_2D_AB_Solver
    )
    size = 5
    for field in tuple(model.solve(1000))[999:1000]:
        plot_field_2d(field, size=(size, size), colors="viridis")
    """

    def __init__(self, domain: NDArray, solver: Solver, **properties):
        super().__init__(
            name=type(self).__name__, alias="ch_2d_ab", domain=domain, solver=solver
        )
        self.properties = properties

    def solve(self, steps: int = 10_000):
        # dt, R, La, T, ac, Da, Db
        for n in range(steps):
            self._states.append(self.solver(**self.properties, domain=self._states[-1]))
            yield self._states[-1]
