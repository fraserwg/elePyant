import pytest
import elePyant.core as epc
import elePyant.test as ept
import xarray as xr
import os.path as osp

class TestDataArrayFuncs:
    def test_da_compression(self, tmpdir):
        da_path = osp.join(osp.dirname(ept.__file__), 'da_test.nc')
        da = xr.open_dataarray(da_path)

        da_out_path = osp.join(tmpdir, 'da_out.nc')
        epc.compress_dataarray(da, da_out_path, 3)


    def test_ds_rejection(self, tmpdir):
        ds_path = osp.join(osp.dirname(ept.__file__), 'da_test.nc')
        ds = xr.open_dataset(ds_path)

        ds_out_path = osp.join(tmpdir, 'ds_rejec_out.nc')
        with pytest.raises(AssertionError):
            epc.compress_dataarray(ds, ds_out_path, 3)
