# -*- coding: utf-8 -*-

import warnings
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from matplotlib import animation
from numpy.random import rand
from overrides import overrides
from tqdm import tqdm_notebook as tqdm

warnings.filterwarnings("ignore", category=RuntimeWarning)

from microtex.modeling import Model2D


class Ising_Lattice_2D_AB_Model(Model2D):
    """
    Sample an equilibrium state of the Ising model on square lattice with
    Glauber or Kawasaki dynamics with periodic boundary condition.

    :param N: Number of lattice sites.
    :param kinetics: Kawasaki or Glauber dynamics.
    :param temp_point: Temperature
    :param beta: The inverse temerature 'beta' Boltzmann parameter.
    :param config: The configuration.
    :param low_T: ...
    :param high_T: ...

    :param equstep:
    :param calcstep:
    """

    def __init__(self, N, temp, kinetics, temp_point, temp_range, equistep, calcstep):

        super().__init__(
            name="Ising Lattice 2D",
            alias="ising2D",
            domain=None,
            solver=None,
            config=None,
        )

        self.N = N
        self.kinetics = kinetics
        self.temp_point = temp_point
        self.beta = 1.0 / temp
        self.state = 2 * np.random.randint(2, size=(N, N)) - 1

        self.low_T = temp_range[0]
        self.high_T = temp_range[1]

        self._size = (N, N)

        self.equistep = equistep
        self.calcstep = calcstep

        # Divide by number of samples, and by system size to get intensive values
        # self.n1 = 1.0 / (calcstep * N * N)
        # self.n2 = 1.0 / (calcstep * calcstep * N * N)

        self.energy = 0
        self.magnet = 0
        self.energy2 = 0
        self.magnet2 = 0

        # Temperature, Energy, Magnetization, Heat Capacity, Succeptibility.
        self.T = np.linspace(temp_range[0], temp_range[1], temp_point)
        self.E = np.zeros(temp_point)
        self.M = np.zeros(temp_point)
        self.C = np.zeros(temp_point)
        self.X = np.zeros(temp_point)

    @property
    def size(self) -> Tuple[int, int]:
        """
        :return: the lattice size i.e number of rows and columns ``[r, c]``.
        """
        return self._size

    # def calculate_energy(self):
    #     E_config = 0
    #     for i in range(self.N):
    #         for j in range(self.N):
    #             spin = self.state[i, j]
    #             bottom = self.state[(i + 1) % self.N, j]
    #             right = self.state[i, (j + 1) % self.N]
    #             left = self.state[(i - 1) % self.N, j]
    #             top = self.state[i, (j - 1) % self.N]
    #             neighbours = bottom + right + left + top
    #             E_config += -spin * neighbours
    #     return E_config / 4

    # def calculate_magnetisation(self):
    #     return np.sum(self.state)

    # def calculate_statistics(self):
    #     self.magnet += self.calculate_magnetisation()
    #     self.energy += self.calculate_energy()
    #     self.magnet2 += self.calculate_magnetisation() ** 2
    #     self.energy2 += self.calculate_energy() ** 2

    #     return self.magnet, self.energy, self.magnet2, self.energy2

    # def analyse(self):
    #     for tempstep in tqdm(range(self.temp_point)):
    #         self.beta = 1.0 / self.T[tempstep]

    #         for i in range(self.equistep):  # equilibrate
    #             self.monte_carlo_step()  # Monte Carlo moves

    #         for i in range(self.calcstep):
    #             self.monte_carlo_step()
    #             self.get_stats()

    #         self.E[tempstep] = self.n1 * self.energy
    #         self.M[tempstep] = self.n1 * self.magnet
    #         self.C[tempstep] = (
    #             (self.n1 * self.energy2 - self.n2 * self.energy * self.energy)
    #             * self.beta
    #             * self.beta
    #         )
    #         self.X[tempstep] = (
    #             (self.n1 * self.magnet2 - self.n2 * self.magnet * self.magnet)
    #             * self.beta
    #             * self.beta
    #         )
    #         self.reinitialise_properties()

    def different_lattice(self):
        """
        Get different lattices i and j (JIT cant do while loops).
        Used in `kawasaki` method.
        """
        spin_1, spin_2 = 0, 0
        while spin_1 == spin_2:
            # Choose randomly 2 dinstinct sites i & j
            row_1, col_1 = np.random.randint(0, self.N), np.random.randint(0, self.N)
            row_2, col_2 = np.random.randint(0, self.N), np.random.randint(0, self.N)
            spin_1, spin_2 = self.state[row_1, col_1], self.state[row_2, col_2]

        return ((row_1, col_1), (row_2, col_2))

    def glauber(self) -> None:
        """
        Simulate one time step with Glauber kinetics.
        """
        for i in range(self.N):
            for j in range(self.N):
                row, col = np.random.randint(0, self.N), np.random.randint(0, self.N)
                spin = self.state[row, col]

                # Finding nearest neighbour with periodic boundary condition.
                bottom = self.state[(row + 1) % self.N, col]
                right = self.state[row, (col + 1) % self.N]
                left = self.state[(row - 1) % self.N, col]
                top = self.state[row, (col - 1) % self.N]

                neighbours = bottom + right + left + top

                # Calculate ∆E = E_nu - E_mu = 2E_nu
                delta_e = 2 * spin * neighbours

                # If ∆E ≤ 0, spin flip always flipped
                if delta_e < 0:
                    spin *= -1

                # Else, flipped with P = exp(-∆E/kT)
                elif rand() < np.exp(-delta_e * self.beta):
                    spin *= -1

                self.state[row, col] = spin

    def kawasaki(self) -> None:
        """
        Simulate one-time step with Kawasaki dynamics.
        """
        for i in range(self.N):
            for j in range(self.N):
                # Choose the random spins.
                r1, c1 = np.random.randint(0, self.N), np.random.randint(0, self.N)
                r2, c2 = np.random.randint(0, self.N), np.random.randint(0, self.N)
                s1, s2 = self.state[r1, c1], self.state[r2, c2]

                # Check if cells are same, if so, choose other spins.
                if r1 == r2 and c1 == c2:
                    ((r1, c1), (r2, c2)) = self.different_lattice()
                    s1, s2 = self.state[r1, c1], self.state[r2, c2]

                # Consider the exchange as two consecutive single spin flips.
                # Find the nearest neighbor with periodic boundary conditions.

                # top, right, bottom, left neighbours
                t1 = self.state[r1, (c1 - 1) % self.N]
                t2 = self.state[r2, (c2 - 1) % self.N]

                r1 = self.state[r1, (c1 + 1) % self.N]
                r2 = self.state[r2, (c2 + 1) % self.N]

                b1 = self.state[(r1 + 1) % self.N, c1]
                b2 = self.state[(r2 + 1) % self.N, c2]

                l1 = self.state[(r1 - 1) % self.N, c1]
                l2 = self.state[(r2 - 1) % self.N, c2]

                n1 = b1 + r1 + l1 + t1  # neighbour 1
                n2 = b2 + r2 + l2 + t2  # neighbour 2

                # Calculate ∆E as a sum of E changes for 2 moves separately.
                ΔE = (2 * s1 * n1) + (2 * s2 * n2)

                # If ΔE decreased then exchange is made, else the exchange is made with P = exp(-∆E/kT)
                if ΔE < 0:
                    s1 *= -1
                    s2 *= -1
                    # print("flip A")
                elif rand() < np.exp(-ΔE * self.beta):
                    s1 *= -1
                    s2 *= -1
                    # print("flip B")
                self.state[r1, c1], self.state[r2, c2] = s1, s2

        # print(self.T)

    @overrides
    def solve(self) -> "array":
        """
        Monte Carlo simulation step to modify lattice with selected kinetics.
        """
        try:
            getattr(self, self.kinetics)()
            # self.kawasaki()
            # print(f"{i + 1}. SIMULATION DONE")
        except Exception:
            raise IsingError("Unknown kinetics given.")
        return self.state.copy()  # MUST be copy!
