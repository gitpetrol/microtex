# -*- coding: utf-8 -*-

"""
The model classes and functions.

# TODO Typecheck shape and dtype of NDArray
"""

from __future__ import annotations

import pickle
from abc import ABC, abstractclassmethod, abstractmethod
from os import PathLike
from typing import Iterable, Optional, Protocol, Type

import numpy as np
from numpy.typing import NDArray

from microtex.modeling._solver import Solver, Solver1D, Solver2D, Solver3D

__all__ = tuple(
    [
        "make_samples",
        "ModelLike",
        "ModelND",
        "Model1D",
        "Model2D",
        "Model3D",
        "ModelError",
        "Configuration",
    ]
)


def make_samples(min: int, max: int, count: int) -> Iterable[int]:

    """
    Make a geometrically spaced integers from minimum to maximum.
    """
    return np.array(np.geomspace(min, max, num=count, dtype="uint")).tolist()


class Configuration(ABC):
    """
    The configuration abstract class.
    You must derive this class for each model and pass a model type and configuration values.
    """

    def __init__(self, model: Type, **kwargs):
        self._model = model.__name__()
        self._values = dict(**kwargs)

    @property
    def model(self) -> str:
        """
        Get the model name.
        """
        return self._model

    @property
    def values(self):
        """
        Get the configuration values.
        """
        return self._values

    def __eq__(self, that: object) -> bool:
        return (
            isinstance(self, that)
            and self.model == that.model
            and self.values == that.values
        )

    def __hash__(self) -> int:
        return hash((type(self), self.model, self.values))


class ModelLike(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def alias(self) -> str:
        ...

    @property
    def solver(self) -> str:
        ...

    @property
    def config(self) -> Optional[Configuration]:
        ...


class ModelError(Exception):
    """
    An exception class for models.
    """


class ModelND(ABC):
    """
    Abstract base class for models.

    The model object can be statefull or stateless. The model instance is created with
    the approriate initial domain (1D, 2D, 3D) and for the each time step the solver
    returns a new array. This array then appended to the `states` attribute. If you need
    to store only the initial and final state, you have to specify it in configuration,
    otherwise all states are stored i.e that you need a lot of computer memory for a
    large numpy arrays.
    """

    def __init__(
        self,
        name: str,
        alias: str,
        domain: NDArray,
        solver: Solver,
        config: Configuration = None,
    ) -> None:
        """
        When no configuration is provided the model should provide sensible default configuration.
        """
        self._name = name
        self._alias = alias
        self._states = [
            domain,
        ]
        self._solver = solver
        self._config = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def solver(self) -> str:
        return self._solver

    @property
    def config(self) -> Optional[Configuration]:
        return self._config

    @abstractmethod
    def solve(self):
        """
        Solve the model i.e., make time step.
        """

    def save(state: NDArray, path: PathLike) -> None:
        """
        Save the model state to file.
        """
        with open(path, "wb") as f:
            pickle.dump(state, f)

    def load(cls, pickle_path: PathLike) -> ModelND:
        """
        Load the model state from file.
        """
        with open(pickle_path, "rb") as f:
            conf, state = None, pickle.load(f)  # FIXME None conf
            return cls()


class Model1D(ModelND):
    """
    Abstract base class for 1D models.
    """

    def __init__(
        self, name: str, alias: str, domain: NDArray, solver: Solver1D, config=None
    ) -> None:
        super().__init__(
            name=name, alias=alias, domain=domain, solver=solver, config=config
        )


class Model2D(ModelND):
    """
    Abstract base class for 2D models.
    """

    def __init__(
        self, name: str, alias: str, domain: NDArray, solver: Solver2D, config=None
    ) -> None:
        super().__init__(
            name=name, alias=alias, domain=domain, solver=solver, config=config
        )
        if domain.ndim != 2:
            raise ValueError("Domain dimension must be equal to 2.")

    @property
    def nx(self) -> int:
        """
        :return: The number of points in `x` direction.
        """
        return self._size[0]

    @property
    def ny(self) -> int:
        """
        :return: The number of points in `y` direction.
        """
        return self._size[1]


class Model3D(ModelND):
    """
    Abstract base class for 3D models.
    """

    def __init__(
        self, name: str, alias: str, domain: NDArray, solver: Solver3D, config=None
    ) -> None:
        super().__init__(
            name=name, alias=alias, domain=domain, solver=solver, config=config
        )
