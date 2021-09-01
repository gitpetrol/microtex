# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path

import h5py
import numpy as np


__all__ = tuple(["HDF5Writer", "HDF5Reader"])


class HDF5Writer:
    """
    Simple class to store results in a HDF5 file.

    Params:
        filename: filepath of h5 file
        data: initial array
        shape: dataset shape (not counting main/batch axis)
        dtype: numpy dtype (default np.float32)
        compression: compression filter (default 'gzip')

    Usage:
        # create store according to initial array field_i
        hdf5_store = HDF5Writer('/tmp/hdf5_store.h5', field_i)
        # append further results
        hdf5_store.append(field_1, timestep=1)
        hdf5_store.append(field_2, timestep=2)

    """

    def __init__(self, filename, data, config, **kwargs):
        self.filename = filename
        self.shape = data.shape
        self.i = 1
        dtype = kwargs.get('dtype', np.float32)
        compression = kwargs.get('compression', 'gzip') 

        with h5py.File(self.filename, mode="w") as h5f:
            dset = h5f.create_dataset(
                "fields",
                maxshape=(None,) + self.shape,
                dtype=dtype,
                compression=compression,
                chunks=True,
                data=data[np.newaxis, :, :],
            )
            for key in config.keys():
                dset.attrs[key] = getattr(config, key)
            dset.attrs["timesteps"] = [0]
            timenow = datetime.now().isoformat()
            dset.attrs["created"] = timenow
            dset.attrs["modified"] = timenow

    def append(self, field, timestep=None):
        if timestep is None:
            timestep = self.i
        with h5py.File(self.filename, mode="a") as h5f:
            dset = h5f["fields"]
            dset.resize((self.i + 1,) + self.shape)
            dset[self.i] = field
            dset.attrs["timesteps"] = np.append(dset.attrs["timesteps"], timestep)
            dset.attrs["modified"] = datetime.now().isoformat()
            h5f.flush()
            self.i += 1

    def set_attr(self, key, value):
        with h5py.File(self.filename, mode="a") as h5f:
            dset = h5f["fields"]
            dset.attrs[key] = value
            h5f.flush()

    def del_attr(self, key):
        with h5py.File(self.filename, mode="a") as h5f:
            dset = h5f["fields"]
            if key in dset.attrs:
                del dset.attrs[key]
                h5f.flush()


class HDF5Reader:
    """
    Simple class to read results from HDF5 file using context manager.

    Params:
        filename: filepath of HDF5 file

    Usage:
        df = HDF5Reader('/tmp/hdf5_store.h5')
        print(df.attrs)
        field = df.get_field(32)

        # or as context manager

        with HDF5Reader('/tmp/hdf5_store.h5') as hdf5
            dset = hdf5['fields']
            ...

    """
    def __init__(self, filename):
        self.filename = filename
        with h5py.File(self.filename, 'r') as h5f:
            dset = h5f['fields']
            self.attrs = dict(dset.attrs)
        self.file = None

    def get_field(self, timestep):
        with h5py.File(self.filename, 'r') as h5f:
            return h5f['fields'][timestep]

    def __enter__(self):
        self.file = h5py.File(self.filename, 'r')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


def search_simulations(wdir, **kwargs):
    """Search for HDF5 simulation files using attributes"""
    res = []
    for p in Path(wdir).iterdir():
        if p.is_file():
            try:
                df = HDF5Reader(p)
                if all(item in df.attrs.items() for item in kwargs.items()):
                    res.append(p)
            except OSError:
                pass

    return res
