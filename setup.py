# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


if __name__ == "__main__":

    exec(open('src/microtex/__init__.py').read())

    PACKAGE_NAME = "microtex"
    setup(
        name=PACKAGE_NAME,
        version= __version__,
        package_dir={"": "src"},
        py_modules=[],
        packages=find_packages(),
        install_requires=[
            "tqdm",
            "numpy>=1.21",
            "numba",
            "scipy",
            "overrides",
            "matplotlib",
            "h5py",
        ],
        extras_require={
            "lint": ["black", "isort", "flake8"],
            "test": ["pytest"],
            "notebook": ["ipykernel", "notebook"]
        },
        entry_points={
            "console_scripts": [
                f"{PACKAGE_NAME}={PACKAGE_NAME}.__main__:main"
            ]
        },
    )
