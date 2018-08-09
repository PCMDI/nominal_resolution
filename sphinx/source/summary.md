# Summary

To provide users with a searchable label identifying the approximate horizontal grid resolution of data reported for CMIP6 experiments, an algorithm was devised that defines what is called the "nominal resolution".  The nominal resolution is recorded in each model output file, and then harvested by ESGF (which archives and serves the CMIP6 data) so that the resolution can be used as one of the search criteria.  

The algorithm for defining nominal resolution is given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi) of a data specifications document for CMIP6.  For regular cartesian latitude by longitude global grids, a formula given in [Appendix 2](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi) can be used, but for rotated pole grids, irregular grids, sub-global domains, and the like, a computer calculation is required.  The code available here can be used for that purpose.

Note that the nominal_resolution is used to characterize the resolution of the grid used to report model output fields, which may differ from the native grid on which the fields are calculated by the model.

For the most common use case, a user must call the function nominal_resolution.mean_resolution, providing an array containing grid-cell areas and arrays containing the longitude and latitude coordinates of the vertices of each grid cell.  The function returns the nominal resolution (a string such as "25 km", "50 km", "100 km", etc.).  The input arrays are dimensioned as follow:
cell_area[n]
lat_vert[n,maxv]
lon_vert[n,maxv]
Any sensible unit can be used in defining cell_areas (including non-dimensional angular area measures).  The longitudes and latitudes should be expressed either in radians or degrees (limits ???   -90 to 90 or 90 to -90 ;  0 to 360 or -180 to 180 ????)

