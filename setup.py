from setuptools import setup

setup(
    name='elePyant',
    version='0.0.2',
    author='Fraser Goldsworth',
    author_email='fraser.goldsworth@physics.ox.ac.uk',
    packages=['elePyant', 'elePyant.test'],
    scripts=[],  # ['bin/<<script_name>>]
    data_files=['elePyant/test/da_test.nc','elePyant/test/ds_test.nc'],
    url='https://github.com/fraserwg/elePyant/releases/tag/v0.0.2',
    download_url='https://github.com/fraserwg/elePyant/archive/v0.0.2.tar.gz',
    license='LICENSE',
    description='Package that performs compression by rounding.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['xarray', 'numpy', 'h5netcdf'],
)
