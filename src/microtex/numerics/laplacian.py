import numpy as np
import scipy.sparse as sp
from numpy import zeros
from scipy.linalg import toeplitz
from scipy.sparse import eye, kron


def laplacian_2d(nx, ny, dx, dy):
    """
    The laplacian matrix for 2D schema.

    Example:
        >>> laplacian_2d(2, 2, 0.1, 0.1).todense()

    :return: the Laplacian matrix.
    """
    D = np.ones([nx * ny])
    M = sp.spdiags([D, -2 * D, D], [-1, 0, 1], nx, ny)
    I = sp.eye(nx * ny)

    return sp.kron(I, M, format="csr") + sp.kron(M, I)
