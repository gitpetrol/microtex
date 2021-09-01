# -*- coding: utf-8 -*-


from microtex.modeling.cahn_hilliard._model import (
    Cahn_Hilliard_2D_AB_Model as Cahn_Hilliard_2D_AB_Model
)

from microtex.modeling.cahn_hilliard._solver import (
    Configuration as Configuration,
    Cahn_Hilliard_2D_AB_Solver as Cahn_Hilliard_2D_AB_Solver,
)


__all__ = tuple([
        "Configuration",
        "Cahn_Hilliard_2D_AB_Model",
        "Cahn_Hilliard_2D_AB_Solver",
])
