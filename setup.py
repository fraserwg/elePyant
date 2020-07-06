from setuptools import setup

setup(
    name='elePyant',
    version='0.0.1',
    author='Fraser Goldsworth',
    author_email='fraser.goldsworth@physics.ox.ac.uk',
    packages=['elePyant', 'elePyant.test'],
    scripts=[],  # ['bin/<<script_name>>]
    # url='http://pypi.python.org/pypi//',
    license='LICENSE',
    description='An awesome package that does something',
    long_description=open('README.md').read(),
    install_requires=[],  # Need to add requirements
)
