# MicroTEX

[![black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)

__MicroTEX is a package for material microstructure and microtexture simulations.__

## Description

The package contains several classes to simulate the evolution of symplectic microstructure,
particularly it contains solvers for several models of exsolution in binary solid solution. To be able to understand what is going under the hood and to be able to create or customize your model you should to know the basics of scientific Python stack, e.g., NumPy, SciPy, Matplotlib, Numba packages.

### Features

- [x] The Cahn-Hilliard 2D phase-field model of spinodal decomposition.
- [ ] The Ising lattice model 2D mean-field model of spinodal decomposition.
- [ ] Be able to observe, pause and resume the running simulation.
- - [ ] Run multiple simulations in simultaneously / in paralell.
  - Use multiprocessing or threading?
- [ ] Be able to see progress (image) when te simulation is running: producer/consumer pattern?
  Use some message queue such as (Celery | Dramatique) + Redis?

## Installation

Before the installation, you should create and activate the virtual environment!
You can create a virtual environment with [venv](https://docs.python.org/3/library/venv.html) module or with help of [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

 The `venv` module is distributed with Python by default on Windows but on Ubuntu you have to install it by yourself as an separate package, search for `python3-venv` package.

Install directly from the `git` repository.

```bash
pip install git+https://github.com/groundf/thesis-prf-bs
```

or clone and install the package with

```bash
git clone git+https://github.com/groundf/thesis-prf-bs
pip install thesis-prf-bs
```

For development, clone the repository and install the package in editable mode with additional development packages.

```bash
pip install -e ".[test, lint, notebook]"
```

The editable mode is MUST for running notebook in VS Code!
Notebooks can be very large after execution, be sure that the size is reduced before push (restart notebook and maybe empty cells).

Chek the size of files (Powerbash):

```bash
git ls-tree -r -l --abbrev --full-name HEAD | Sort-Object {[int]($_ -split "\s+")[3]} | Select-Object -last 10
```

See this StackOverflow [answers](https://stackoverflow.com/questions/9456550/how-to-find-the-n-largest-files-in-a-git-repository).

## Execution

```bash
microtex <options + flags>
```

The initial settings for simulations can be loaded from specified input file folder and the outputs can be saved specified output folder.When using a package you must specify these folders with command options `--input` (`-i`) and `--output` (`-o`).

```bash
microtext -i path/to/input/file -o path/to/output/folder
```

## Architecture

The central classes of the package is `Simulation` class which takes model object and runs the simulation according to the configuration.
The `Simulation` is an abstract class from which a classes representing a concrete simulation must derive. The simulation object contains
special method which runs the model time step. How many steps we run, is the responsibility of this object. The `Simulation` also
takes the responsibility of sending the results of the simulation to other systems. This add flexibility to consume the results continuously e.g., we can save a plot for each `n` steps to observe a results when simulation is still running. We can also pause and resume the simulation.

Every model is represented by a standalone class that is responsible for setting up and solving the coresponding
model.


## Notes

- https://towardsdatascience.com/stop-using-numpy-random-seed-581a9972805f