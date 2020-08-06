""" elePyant.core

Core functions of elePyant.

Contains methods:
    compress_dataarray --> For compressing xarray.DataArray objects.
    compress_dataset --> For compressing xarray.Dataset objects.
    compress_netcdf --> For compressing netCDF files stored on the disk.
"""
import xarray as xr
import numpy as np


def _round_dsd_base10(x, dsd):
    """Round to preserve decimal places (in base 10).
    
    Parameters
    ----------
    x : numpy.ndarray
    dsd : int
        decimal significant digits
        positive to the right of decimal point, negative to the left
        
    Returns
    -------
    numpy.array
        rounded array
    """
    # original elePyant method
    return np.around(x, decimals=dsd)


def _round_nsd_base10(x, nsd):
    """Round to preserve sig figs (in base 10).

    Parameters
    ----------
    x : numpy.ndarray
    nsd : int
        number of significant digits (sig figs)

    Returns
    -------
    numpy.array
        rounded array
    """
    where_zero = x == 0  # avoid taking log10 of 0
    tens = np.ones_like(x)
    tens[~where_zero] = 10 ** np.ceil(np.log10(np.abs(x[~where_zero])))
    # note: could instead pass `where=where_zero` to np.abs or np.log etc.
    
    # "true normalized" significand
    # https://en.wikipedia.org/wiki/Significand
    x_sig = x / tens
    
    return np.around(x_sig, decimals=nsd) * tens
    # or could pass to _round_dsd_base10


def round_array(x, nsd=None, dsd=None):
    """Round a NumPy array using selected method.

    Args:
        x (numpy.ndarray)

    """
    if nsd and dsd:
        raise Exception(f"Must set either `nsd` or `dsd`, not both.")

    if nsd:
        return _round_nsd_base10(x, nsd)

    elif dsd:
        return _round_dsd_base10(x, dsd)

    else:
        raise Exception("Must set either `nsd` or `dsd`.")



def round_dataarray(da, *, keep_attrs=True, inplace=False, **kwargs):
    """Round an xarray.DataArray

    Args:
        da (xarray.DataArray): Data array to be rounded

        keep_attrs (bool): Whether to preserve the original attributes
        inplace (bool): W
            note `inplace` was deprecated in xarray
            (https://github.com/pydata/xarray/issues/1756)

        kwargs : passed on to ``round_array``

    """
    # optionally inplace?
    assert isinstance(da, xr.DataArray)

    da_rounded[:] = round_array(da.values, **kwargs)

    if not keep_attrs:
        da_rounded.attrs = {}

    return da_rounded


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

    assert isinstance(da, xr.DataArray)
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
        ignore_vars (str or list): Should only be set if decimal_places is int. Gives
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
    assert isinstance(ds, xr.Dataset)  # This may mess with duck typing.

    if isinstance(decimal_places, int):
        decimal_places = {var: decimal_places for var in ds.data_vars}

    assert isinstance(decimal_places, dict)

    if ignore_vars is not None:
        if isinstance(ignore_vars, str):
            ignore_vars = [ignore_vars]

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
