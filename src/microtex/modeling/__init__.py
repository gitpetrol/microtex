# -*- coding: utf-8 -*-

"""
Cahn-Hilliard 2D model and solver implemented with a finitie difference method.

.. note::
    The implemetation use two for loops which is, on the one hand, very slow compared to methods using
    sparse matrix e.g from SciPy package, but on other hand, very simple and easy to follow for novices.
    The computation were really horrible to the time we had used JIT (Just-in-Time) directive from Numba
    package. This simple addition was able to speedup the code 10 times. If you have better performing
    solver, you can simply swap our implementation with yours when instantiating the model object. You can
    even implemnet your model in C++ or Fortran with Python interface.

The solvers can be any callable i.e that you can implemented as simple function or object (functor) with
`__call__` method.
with signature :code:`Callable[[], NDArray]`. There is a protocol names :code:`Solver`. It takes configuration
and input state (array) and returns the output state (array). This means that solver represent a one time step
of your model. How many steps you want to make is not responsibility
of the solver.

.. code-block::python

    from microtex.modeling import Cahn_Hilliard_2D_AB_Solver
    from microtex.modeling import Cahn_Hilliard_2D_AB_Solver_Fast
"""

from microtex.modeling._model import Configuration as Configuration
from microtex.modeling._model import Model1D as Model1D
from microtex.modeling._model import Model2D as Model2D
from microtex.modeling._model import Model3D as Model3D
from microtex.modeling._model import ModelError as ModelError
from microtex.modeling._model import ModelND as ModelND
from microtex.modeling._model import make_samples as make_samples
from microtex.modeling._solver import Solver as Solver

__all__ = tuple(
    [
        "make_samples",
        "ModelND",
        "Model1D",
        "Model2D",
        "Model3D",
        "Solver",
        "Configuration",
    ]
)
