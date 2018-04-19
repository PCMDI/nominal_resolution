from distutils.core import setup

Version="0.0.1"

setup (name = "nominal_resolution",
       author="AIMS Team",
       version=Version,
       description = "Utilities for E3SM NEx grids",
       url = "http://github.com/cdat/nominal_resolution",
       packages = ['nominal_resolution'],
       package_dir = {'nominal_resolution': 'lib'},
       #data_files = [ ("share/nominal_resolution",("share/nominal_resolution.nc",))],
       #scripts= ["scripts/nominal_resolution"],
      )
    
