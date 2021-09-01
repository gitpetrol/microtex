# -*- coding: utf-8 -*-

import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

from microtex.storage import HDF5Reader  # used by `plot_field_grid()``

__all__ = tuple(["plot_field_2d", "plot_field_grid", "lot_density_vs_free_energy"])


def plot_field_2d(data, size=(10, 10), colors="bwr", minmax=(0, 1)):
    fig, axs = plt.subplots(figsize=size)
    # figsize=size, constrained_layout=True
    psm = axs.pcolormesh(
        data, cmap=colors, rasterized=True, vmin=minmax[0], vmax=minmax[1]
    )
    fig.colorbar(psm, ax=axs)
    plt.show()


def plot_density_vs_free_energy(c0, T0, omega, **kwargs):
    import numpy as np
    from microtex.quantities import R
    import matplotlib.pyplot as plt
    size = kwargs.get('figsize', (5, 5))
    fig = plt.figure(figsize=size)
    cc = np.linspace(0.01, 0.99, 100)
    # Set functional F as parameter and don't calculate here!
    for T in T0:
        plt.plot(cc, R * T * (cc * np.log(cc) + (1 - cc) * np.log(1 - cc)) + omega * cc*(1 - cc), label=f"{T} (K)")
        plt.plot(c0, R * T * (c0 * np.log(c0) + (1 - c0) * np.log(1 - c0)) + omega * c0*(1 - c0),color='black',marker='o',markersize=5)
    plt.xlabel('c(x)')
    plt.ylabel('f(c)')
    plt.legend(title="T", loc="upper right")

    plt.show()


def make_animation(frames, frame_count, heigh, width):
    # Create an animation from the given frames.

    figure = mp.figure()

    mp.title("LIFE", y=1.02, fontsize=12)

    frames_ = [
        [mp.imshow(frame, cmap="gray", interpolation="nearest", animated=True)]
        for frame in frames
    ]

    movie = mpa.ArtistAnimation(figure, frames_, blit=True, repeat=True)

    movie.save(f"LIFE_frames({frame_count})_size({height},{width}).mp4", fps=25)

    mp.show()


def plot_field_grid(h5file, steps, nrows=2, ncols=2, filename=None, cmap='viridis', **kwargs):
    """
    Plot 2x2 grid of fields with common colorbar.
    """
    assert len(steps) == nrows * ncols, 'Number of steps must equal to number of axes.'
    normalizer = Normalize(0, 1)
    im = cm.ScalarMappable(norm=normalizer)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, **kwargs)

    with HDF5Reader(h5file) as df:
        dset = df["fields"]
        attrs = dict(dset.attrs)
        for ax, step in zip(axes.flat, steps):
            ax.imshow(dset[step], cmap=cm.get_cmap(cmap), norm=normalizer)
            ax.set_title(f'Time: {attrs["timesteps"][step]}')
            ax.set_axis_off()

    fig.colorbar(im, ax=axes.ravel().tolist())
    if filename is not None:
        plt.savefig(filename)
        plt.close('all')
    else:
        plt.show()
