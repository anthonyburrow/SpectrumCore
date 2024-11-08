from setuptools import setup, find_packages


__version__ = '0.0.1'


setup(
    name='SpecFit',
    version=__version__,
    description='Core spectrum-reading and -processing functions.',
    url='https://github.com/anthonyburrow/SpectrumCore',
    author='Anthony Burrow',
    author_email='anthony.r.burrow@gmail.com',
    license='MIT',
    include_package_data=True,
    install_requires=['numpy', 'matplotlib'],
    # optional=[],
    packages=find_packages(),
    extras_require={'test': 'pytest'},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ]
)
