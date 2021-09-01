# -*- coding: utf-8 -*-

"""
Contains chemical and physical quantitias/constants.
"""

from dataclasses import dataclass

__all__ = tuple(("R"))


# ########################################################################### #
#                               THERMODYNAMICS                                #
# ########################################################################### #


# The universal gas constant (exact) [J/K/mol].
R = 8.31446261815324


@dataclass(frozen=True)
class Work:
    value: float


@dataclass(frozen=True)
class Heat:
    value: float


@dataclass(frozen=True)
class Entropy:
    value: float
    units: str
    symbol: str = "S"


class Quantity:
    ...


@dataclass(frozen=True)
class Enthalpy:
    value: float
    units: str
    symbol: str = "H"

    def __add__(self, other):
        return self.value + other.value


def enthalpy_change(Hi, Hf):
    return Hf - Hi


class EnthalpyOfMixing(Enthalpy):
    ...


"""
Domain model classes -- mostly value objects.
"""


class ScalarField:
    ...


class VectorFirld:
    ...


# Thermodynamic Properties
class PhysicalQuantity:
    ...


class Temperature(PhysicalQuantity):
    ...


class Pressure(PhysicalQuantity):
    ...


class Time:
    ...


class Grid:
    ...


class Phase:
    ...


class LiquidPhase(Phase):
    ...


class SolidPhase(Phase):
    ...


class GassPhase(Phase):
    ...


class Mixture:
    ...


class BinaryMixture(Mixture):
    ...


class SolidSolidMixture(BinaryMixture):
    ...


class Energy:
    ...


class KineticEnergy(Energy):
    ...


class PotentialEnergy(Energy):
    ...


class Microstructure:
    ...


class CahnHilliardEquation:
    ...


class ThermodynamicBarrier:
    ...


class Reaction:
    ...


class SpinodalRegion:
    ...


class DiffusionEquaition:
    ...


class PhaseSeparation:
    ...
