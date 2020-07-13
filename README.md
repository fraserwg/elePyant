# elePyant

elePyant (pronounced elephant) provides a set of tools for compressing netCDF files, and xarray Datasets and DataArrays. It works by ridding data of 'meaningless digits' before saving the rounded dataset as compressed netCDF file.

To give an idea of the performance that can be obtained, I was able to reduce and file from 1 GB in size to 30 MB by using only the functions within this package. No qualitative difference is visible in the dataset.

The compression is based on work by Milan Kloewer. Often when working with data we only 'know' the value of a quantity to several significant figures. When we store it however we save the value as a 32 or 64 bit number, which can save the number using up to 11 decimal places or so. This is clearly overkill. By rounding all digits of surplus precision in our dataset to zero, we create a pattern in the binary used to encode the data. Lossless compression algorithms can then exploit these patterns to reduce the file size.

The compression relies on the user having a good understanding of the data they are working with. It is up to the user to decide the 'true' precision of their dataset so that they can select appropriate rounding. The method of compression may not be suitable for all purposes as the initial rounding stage of the process is lossy.

## Example usage

The functions contained within the package have been designed to work with objects from the xarray ecosystem. For anyone currently using xarray objects in their workflow, making use of the package is incredibly simple. For instance, if one wants to save an xarray dataset, the process is as simple as going from

```python
ds.to_netcdf('output_file')
```

to

```python
import elePyant as ep
ep.compress_dataset(ds, 'output_file', decimal_places=2)
```

The new function takes the dataset, `ds`, rounds all the data variables (but not coordinate variables) within it to two decimal places and then saves the resulting dataset in to the file `'output_file'`. Similar functions exist for `xr.DataArray` objects and netCDF files.

Advanced functionality allows the user to specify the rounding to use for each variable in a netCDF file. Users can also specify which variables not to round. For instance if you had an `xr.Dataset` object containing the data variables `'UVEL'`, `'VVEL` and `'WVEL'`, you may use the following command

```python
ep.compress_dataset(ds, 'out.nc', decimal_places={'UVEL': 2,
                                                        'VVEL': 2,
                                                        'WVEL': 6})
```

which will round both `'UVEL'` and `'VVEL'` to two decimal places, but `'WVEL'` to six. Alternatively you may not wish to round `'WVEL'` at all in which case you could use

```python
ep.compress_dataset(ds, 'out.nc', decimal_places=2, ignore_vars='WVEL')
```

Note that by default coordinates are never rounded. If you wish to round a coordinate, then the argument `decimal_places` must be a dictionary containing the coordinate you wish to round as a key.

## Requirements

The following packages are needed to run elePyant
- numpy
- xarray
- h5netcdf

## Updates and feature requests

If you make a modification to the code you think would be cool to share with the world, I welcome pull requests. Ditto for bugs etc. Alternatively if you have an idea which you think I should implement let me know and I'll se what I can do.
