import xarray as xr
import numpy as np


def compress_dataarray(data_array, out_filename, decimal_places):
    assert type(data_array) is xr.DataArray
    # Check the filename is a path, directory etc.

    da_rounded = np.around(data_array, decimals=decimal_places)

    da_rounded.to_netcdf(out_filename,
                         encoding={da_rounded.name: {'zlib': True}},
                         engine='h5netcdf')


def compress_dataset(data_set, out_filename, decimal_places):
    raise NotImplementedError('Method not yet implemented')