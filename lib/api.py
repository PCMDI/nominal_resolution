from __future__ import print_function
import numpy, numpy.ma
import warnings

try:
    import cdms2
    has_cdms = True
except:
    has_cdms = False


def degrees2radians(data, force=False):
    """Converts data from deg to radians"""
    if data.max() > 20. or force:
        data = data / 180. * numpy.pi
    else:
        warnings.warn("It appears your data is already in radians, not touching it")
    return data


def mean_resolution(cellarea, latitude_bounds=None, longitude_bounds=None, forceConversion=False, returnMaxDistance=False):
    if longitude_bounds is None and latitude_bounds is None and has_cdms:
        try:  # Ok maybe we can get this info from cellarea data
            mesh = cellarea.getGrid().getMesh()
            latitude_bounds = mesh[:,0]
            longitude_bounds = mesh[:,1]
            warnings.warn("You did not pass lat/lon bounds but we could infer them from cellarea")
        except:
            pass

    if longitude_bounds is None or latitude_bounds is None:
        raise RuntimeError("You did not pass lat/lon bounds and couldn't infer them from cellarea")


    latitude_bounds = degrees2radians(latitude_bounds, forceConversion)
    longitude_bounds = degrees2radians(longitude_bounds, forceConversion)

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
            del_lons = numpy.ma.where(numpy.ma.greater(del_lons,180.),numpy.ma.absolute(del_lons-360.), del_lons)
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

    # Compute nominal resolution based on: https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit#bookmark=id.ibeh7ad2gpdi
    # Link date: Apr 19th, 2018 at 15:43
    nominal_resolutions = [0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0, 5000.0, 10000.0]
    thresholds = [0.72, 1.6, 3.6, 7.2, 16.0, 36.0, 72.0, 160.0, 360.0, 720.0, 1600.0, 3600.0, 7200.0]

    nominal = nominal_resolutions[-1]
    for i, res in enumerate(thresholds):
        if mean_resolution < res:
            nominal = nominal_resolutions[i]
            break

    return "{:g} km".format(nominal)





