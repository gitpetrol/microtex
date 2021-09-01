# -*- coding: utf-8 -*-

"""
work-in-progress
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from numpy.typing import NDArray

__all__ = tuple(["Configuration"])


@dataclass(frozen=True)
class Result:
    data: NDArray
    info: Dict

@dataclass(frozen=True)
class Domain:
    nx: float
    ny: float
    dx: float
    dy: float
    dt: float