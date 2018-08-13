from __future__ import print_function
import numpy, numpy.ma
import warnings

try:
    import cdms2
    has_cdms = True
except:
    has_cdms = False


def degrees2radians(data, radianLimit):
    """Converts data from deg to radians
    
    If no data is outside the range -radianLimit to + radianLimit, assume data is 
                     already in radians and do nothing

    :Example:
        .. doctest:: 

            >>> data = nominal_resolution.degrees2radians(data)

    :param data: array to potentially convert from degrees to radians
    :type data: cdms2.tvariable.TransientVariable
    
    :param radianLimit: If the magnitude of any data value exceeds radianLimit, convert data from deg to rad. 
    :type radianLimit: scalar

    :return: The same data converted from degrees to radians
    :rtype: `cdms2.tvariable.TransientVariable`_
    """
    if numpy.ma.absolute(data).max() > radianLimit:
        data = (data / 180.) * numpy.pi
    else:
        warnings.warn("It appears your data is already in radians, so nothing done by function degrees2radians")
    return data


def mean_resolution(cellarea, latitude_bounds=None, longitude_bounds=None, convertdeg2rad, returnMaxDistance=False):
    """Computes mean nominal resolution

    formula from: https://en.wikipedia.org/wiki/Great-circle_distance

    :Example:
        .. doctest:: 

            >>> mean = nominal_resolution.mean_resolution(cellarea, latitude_bounds=None, longitude_bounds=None, forceConversion=False, returnMaxDistance=False)

    :param cellarea: simple array, python masked array, or cdms2 variable containing area of each cell
    :type cellarea: `cdms2.tvariable.TransientVariable`_

    :param latitude_bounds: 2D numpy-like array containing latitudes vertices (ncell, nvertices). If not passed
                            and cdms2 is available, will try to obtain from cellarea grid
    :type latitude_bounds: `numpy.ndarray`_

    :param longitude_bounds: 2D numpy-like array containing longitudes vertices (ncell, nvertices). If not passed
                            and cdms2 is available, will try to obtain from cellarea grid
    :type longitude_bounds: `numpy.ndarray`_

    :param convertdeg2rad: set to True if lat/lon in degrees; set to false if in radians
    :type convertdeg2rad: `bool`_

    :param returnMaxDistance: Returns an array representing the maximum distance (in km) between vertices for each cell
    :type returnMaxDistance: `bool`_

    :return: the mean nominal resolution in km and optionally the maximum distance array
    :rtype: `float [,cdms2.tvariable.TransientVariable]`_
    """

    if longitude_bounds is None and latitude_bounds is None and has_cdms:
        try:  # Ok maybe we can get this info from cellarea data
            mesh = cellarea.getGrid().getMesh()
            latitude_bounds = mesh[:,0]
            longitude_bounds = mesh[:,1]
            warnings.warn("You did not pass lat/lon bounds but we inferred them from cellarea")
        except:
            pass

    if longitude_bounds is None or latitude_bounds is None:
        raise RuntimeError("You did not pass lat/lon bounds and couldn't infer them from cellarea")

    if convertdeg2rad:
        radianLimit = 0.        
        latitude_bounds = degrees2radians(latitude_bounds, radianLimit)
        longitude_bounds = degrees2radians(longitude_bounds, radianLimit)

    # distance between successive corners
    nverts = latitude_bounds.shape[-1]
    sh = list(latitude_bounds.shape[:-1])
    del_lats = numpy.ma.zeros(sh,dtype=numpy.float)
    del_lons = numpy.ma.zeros(sh, dtype=numpy.float)
    max_distance = numpy.ma.zeros(sh, dtype=numpy.float)

    for i in range(nverts-1):
        for j in range(i+1, nverts):
            del_lats = numpy.ma.absolute(latitude_bounds[:,i] - latitude_bounds[:,j])
            del_lons = numpy.ma.absolute(longitude_bounds[:,i] - longitude_bounds[:,j] )
            del_lons = numpy.ma.where(numpy.ma.greater(del_lons,numpy.pi),numpy.ma.absolute(del_lons-2.*numpy.pi), del_lons)
            # formula from: https://en.wikipedia.org/wiki/Great-circle_distance
            distance = 2.* numpy.ma.arcsin(numpy.ma.sqrt(numpy.ma.sin(del_lats/2.)**2 + numpy.ma.cos(latitude_bounds[:,i])*numpy.ma.cos(latitude_bounds[:,j])*numpy.ma.sin(del_lons/2.)**2))
            max_distance = numpy.ma.maximum(max_distance, distance.filled(0.0))

    radius = 6371.  # in km
    accumulation = numpy.ma.sum(cellarea*max_distance) * radius / numpy.ma.sum(cellarea)
    if returnMaxDistance:
        return accumulation, max_distance*radius
    else:
        return accumulation

def nominal_resolution(mean_resolution):
    """Compute nominal resolution based on: https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi
    # Link date: Apr 19th, 2018 at 15:43

    :Example:
        .. doctest:: 

            >>> nom = nominal_resolution.nominal_resolution(mean_resolution)

    :param mean_resolution: The computed mean resolution for the model's grid
    :type mean_resolution: `float`_

    :return: The nominal resolution
    :rtype: `str`_

"""
    nominal_resolutions = [0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0, 5000.0, 10000.0]
    thresholds = [0.72, 1.6, 3.6, 7.2, 16.0, 36.0, 72.0, 160.0, 360.0, 720.0, 1600.0, 3600.0, 7200.0]

    nominal = nominal_resolutions[-1]
    for i, res in enumerate(thresholds):
        if mean_resolution < res:
            nominal = nominal_resolutions[i]
            break

    return "{:g} km".format(nominal)
