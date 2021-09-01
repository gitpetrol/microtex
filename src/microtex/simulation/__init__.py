# -*- coding: utf-8 -*-

"""
Contains a ``Simulation`` class.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any
from uuid import UUID

from microtex.modeling import Model

__all__ = tuple(["Simulation"])


class Simulation:
    """
    Simulation represents a computer experiment which drives and control a models time evolution.
    """

    def __init__(self, id: UUID, name: str, model: Model, settings: Any) -> None:
        self.id = id
        self.name = name
        self.model = model
        self.settings = settings
        self.should_finish: bool = False
        self.result = []

    def __eq__(self, that: object) -> bool:
        return isinstance(self, type(that)) and self.id == that.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def run(self, stop_function=None) -> "Generator[FIXME]":
        while not self.should_finish:
            result.append((self.model()))


from threading import Thread


class Executor(Thread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        try:
            for n in tqdm(range(1, ns + 1)):
                self.model.solve()
                # yield f"Simulation step {n} for model {model}"
        except Exception as ex:
            raise ex


if __name__ == "__main__":
    print(__doc__)
