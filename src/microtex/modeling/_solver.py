# -*- coding: utf-8 -*-

from typing import Protocol

from numpy.typing import NDArray

__all__ = tuple(["Solver"])


class Solver(Protocol):
    """
    Solver for N-dimensional model.
    """

    def __call__(self, Any, NDArray) -> NDArray:
        ...


class Solver1D(Solver):
    """
    Solver for 1-dimensional models.
    """


class Solver2D(Solver):
    """
    Solver for 2-dimensional models.
    """


class Solver3D(Solver):
    """
    Solver for 3-dimensional models.
    """
