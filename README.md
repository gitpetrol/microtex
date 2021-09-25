# MicroTEX

[![black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)

__MicroTEX is a package for material microstructure and microtexture simulations.__

## Description

The package contains several classes to simulate the evolution of symplectic microstructure,
particularly it contains solvers for several models of exsolution in binary solid solution. To be able to understand what is going under the hood and to be able to create or customize your model you should to know the basics of scientific Python stack, e.g., NumPy, SciPy, Matplotlib, Numba packages.

### Features

- [x] The Cahn-Hilliard 2D (phase-field model of spinodal decomposition).
  - [ ] Spectral method
  - [x] Finite difference method
- [ ] The Ising lattice model 2D (mean-field model of spinodal decomposition).

## Install

Before the installation, you should create and activate the virtual environment!
You can create a virtual environment with [venv](https://docs.python.org/3/library/venv.html) module or with help of [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

 The `venv` module is distributed with Python by default on Windows but on Ubuntu you have to install it by yourself as an separate package, search for `python3-venv` package.

Install directly from the `git` repository.

```bash
pip install git+https://github.com/gitpetrol/microtex
```

or clone and install the package with

```bash
git clone git+https://github.com/gitpetrol/microtex
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

## Execute

```bash
microtex <options + flags>
```

The initial settings for simulations can be loaded from specified input file folder and the outputs can be saved specified output folder.When using a package you must specify these folders with command options `--input` (`-i`) and `--output` (`-o`).

```bash
microtext -i path/to/input/file -o path/to/output/folder
```