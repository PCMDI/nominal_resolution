# Usage Documentation

The purpose of the nominal_resolution python code is to calculate the "nominal resolution" of a horizontal grid.  For CMIP6 the nominal resolution must be calculated the same way for all models.  In the ESGF data archive of CMIP6 results, nominal resolution is one of the search criteria that can be useful in identifying datasets of interest.   

The algorithm for defining nominal resolution is given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi) of a data specifications document for CMIP6.  For regular cartesian latitude by longitude global grids, it can be calculated using a formula given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi), but for irregular grids, sub-global domains, and the like, it must be calculated with python code available here.

Note that the nominal resolution is defined for two different purposes:
* in each CMIP6-archived model output file, a global attribute named `nominal_resolution` is stored, which records the resolution of the **_grid on which data are reported_**
* in the [CMIP6_source_id.json file](https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_source_id.json) the `native_nominal_resolution` is stored, which records the resolution of the **_native grid_** of each model.

For the most common use case, a user must call the function `nominal_resolution.mean_resolution`, providing an array (`cellarea`) containing grid-cell areas and arrays (`latitude_bounds` and `longitude_bounds`) containing the longitude and latitude coordinates of the vertices of each grid cell.  The function returns the nominal resolution (a string such as `25 km`, `50 km`, `100 km`, etc.).  The input arrays can either be simple arrays or numpy masked arrays dimensioned as follow:
```
     cellarea[ncells]
     latitude_bounds[ncells,nverts]
     longitude_bounds[ncells,nverts]
```

where `ncells` is the number of grid cells and `nverts` is the maximum number of vertices a grid cell might have.

Any sensible unit can be used in defining the cell areas (`cellarea`), including non-dimensional angular area measures.  The longitudes and latitudes should be expressed either in radians or in degrees.  For any grid cells with fewer than nverts vertices, the unneeded vertice `longitudes_bounds` and `latitudes_bounds` should either 
* duplicate one of the cell's valid vertex locations
* or be defined as numpy masked arrays with unneeded vertices masked

Depending on the units, the `latitude_bounds` values should be in the range:
* for radians: -pi to pi 
* for degrees: -90. to 90.  If across the entire grid, no latitude is outside the range -16. to 16., then in calling the function `mean_resolution`, you must set parameter `forceConversion` to `True`.

Depending on the units, the `longitude_bounds` values should:
* for radians: span a range no more than 3 pi with the additional restriction that no value should be outside the range -5 pi to 5 pi. 
* for degrees: span a range no more than 540 degrees. If across the entire grid, no longitude is outside the range -16. to 16., then in calling the function `mean_resolution`, you must set parameter `forceConversion` to `True`.


