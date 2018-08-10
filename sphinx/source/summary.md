# nominal_resolution Usage Documentation

The purpose of the nominal_resolution python code is to calculate the "nominal resolution" of a horizontal grid.  For CMIP6 the nominal resolution must be calculated the same way for all models.  In the ESGF data archive of CMIP6 results, nominal resolution is one of the search criteria that can be useful in identifying datasets of interest.   

The algorithm for defining nominal resolution is given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi) of a data specifications document for CMIP6.  For regular cartesian latitude by longitude global grids, it can be calculated using a formula given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi), but for irregular grids, sub-global domains, and the like, it must be calculated with the python code available here (or its equivalent).

Note that the nominal resolution is defined for two different purposes:
* in each CMIP6-archived model output file, a global attribute named `nominal_resolution` is stored, which records the resolution of the **_grid on which data are reported_**
* in the [CMIP6_source_id.json file](https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_id.json) the `native_nominal_resolution` is stored, which records the resolution of the **_native grid_** of each model.

There are two steps in calculating the nominal resolution (for allowed values, see [CMIP6_nominal_resolution.json](https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_nominal_resolution.json)): first, the mean resolution is calculated using the `mean_resolution` function, and then that is passed to the `nominal_resolution` function, which returns `nominal_resolution`.   

For the most common use case, the first step is to call the function `mean_resolution`, passing it an array (`cellarea`) containing grid-cell areas and arrays (`latitude_bounds` and `longitude_bounds`) containing the longitude and latitude coordinates of the vertices of each grid cell.  The input arrays can either be simple arrays or numpy masked arrays dimensioned as follow:
```
     cellarea[ncells]
     latitude_bounds[ncells,nverts]
     longitude_bounds[ncells,nverts]
```

where `ncells` is the number of grid cells and `nverts` is the maximum number of vertices a grid cell might have.

Any sensible unit can be used in defining the cell areas (`cellarea`), including non-dimensional angular area measures.  The longitudes and latitudes should be expressed either in radians or in degrees.  If a grid includes some cells with fewer than `nverts` vertices, the `longitudes_bounds` and `latitudes_bounds` arrays should be defined as numpy masked arrays and any **unneeded** vertices should be masked.

Depending on the units, the `latitude_bounds` values should be in the range:
* for radians: -pi to pi 
* for degrees: -90. to 90.  If across the entire grid, no latitude is outside the range -16. to 16., then in calling the function `mean_resolution`, you must set parameter `forceConversion` to `True`.

Depending on the units, the `longitude_bounds` values should:
* for radians: span a range no more than 3 pi with the additional restriction that no value should be outside the range -5 pi to 5 pi. 
* for degrees: span a range no more than 540 degrees. If across the entire grid, no longitude is outside the range -16. to 16., then in calling the function `mean_resolution`, you must set parameter `forceConversion` to `True`.

The `mean_resolution` is returned by the above function, and, optionally, by setting the function parameter `returnMaxDistance` to `True`, the function will also return an array containing the maximum dimension of each of the grid cells. This array of values could subsequently be used to more fully characterize the distribution of grid cell sizes (allowing the user, for example, to compute a standard deviation). 

If there are grid cells that should be omitted from the calculation, then `cellarea` should be defined as a python masked array (and all omitted cells should be masked). 

The second step is to obtain `nominal_resolution` by passing `mean_resolution` to the `nominal_resolution` function.

The above functions can be found at: https://github.com/PCMDI/nominal_resolution/blob/master/lib/api.py

Sample codes using nominal_resolution are available at: https://github.com/PCMDI/nominal_resolution/tree/master/tests

