import xarray as xr
import numpy as np


def compress_dataarray(da, out_filename, decimal_places):
    """Compressses an xarray.DataArray object.

    Args:
        da (xarray.DataArray): The data array to be compressed.
        out_filename (str or path): The path to save the output to.
        decimal_places (int): The number of decimal places to round the data
            variable to.

    Notes:
        - No rounding is applied to coordinates?
    """

    assert type(da) is xr.DataArray
    # Check the filename is a path, directory etc.

    da_rounded = np.around(da, decimals=decimal_places)

    da_rounded.to_netcdf(out_filename,
                         encoding={da_rounded.name: {'zlib': True}},
                         engine='h5netcdf')


def compress_dataset(ds, out_filename, decimal_places, ignore_vars=None):
    """Compresses an xarray.Dataset object.

    Args:
        ds (xarray.Dataset): The dataset to be compressed.
        out_filename (str or path): The path to save the output file to.
        decimal_places (int or dict): If int, will round each data variable of
            the dataset to that many decimal places. Coordinates are not rounded.
            If dict, keys refer to the data variable or coordinate which is to
            be rounded. Values give the number of decimal places to round to.
            Any unreferenced variables will remain unrounded.
        
    Keyword Args:
        ignore_vars (list): Should only be set if decimal_places is int. Gives
            a list of data variables that shouldn't be rounded. Defaults to
            None. If given when decimal_places is a dict, the code plays
            it safe and removes the items from decimal_places.

    Notes:
        - Applies rounding (lossy) compression only to either data variables or
            variables set in decimal_places.
        - zlib (lossless) compression is applied to all variables regardless
            of whether they are rounded or not.
        - To achieve compression zlib compression must be applied after
            rounding. Otherwise we just have a load of empty bits.
    """
    assert type(ds) is xr.Dataset  # This may mess with duck typing.

    if type(decimal_places) is int:
        decimal_places = {var: decimal_places for var in ds.data_vars}
        
    assert type(decimal_places) is dict

    if ignore_vars is not None:
        for var_to_remove in ignore_vars:
            decimal_places.pop(var_to_remove)

    for variable in decimal_places:
        ds[variable] = np.around(ds[variable],
                                       decimals=decimal_places[variable])

    # Have to turn on lossless compression for each variable in ds.
    encoding = {ds_var: {'zlib': True} for ds_var in ds.variables}

    ds.to_netcdf(out_filename, encoding=encoding, engine='h5netcdf')


def compress_netcdf(in_filename, out_filename, decimal_places, ignore_vars=None):
    """Opens a netCDF file and applies compress_dataset to it.

    Arguments:
        in_filename (str or path): Path to netCDF file to be compressed.

        out_filename (str or path): The path to save the output file to.
        decimal_places (int or dict): If int, will round each data variable of
            the dataset to that many decimal places. Coordinates are not rounded.
            If dict, keys refer to the data variable or coordinate which is to
            be rounded. Values give the number of decimal places to round to.
            Any unreferenced variables will remain unrounded.
        
    Keyword Args:
        ignore_vars (list): Should only be set if decimal_places is int. Gives
            a list of data variables that shouldn't be rounded. Defaults to
            None. If given when decimal_places is a dict, the code plays
            it safe and removes the items from decimal_places.

    Notes:
        - see compress_dataset for more documentation.
    """
    ds = xr.open_dataset(in_filename)
    compress_dataset(ds, out_filename, decimal_places, ignore_vars)
