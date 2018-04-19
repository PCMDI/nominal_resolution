import numpy, numpy.ma
import cdms2
import warnings


def degrees2radians(data, force=False):
    """Converts data from deg to radians"""
    if data.max > 7. or force:
        data = data / 180. * numpy.pi
    return data


def mean_resolution(cellarea, longitude_bounds=None, latitude_bounds=None):
    if longitude_bounds is None and latitude_bounds is None:
        try:  # Ok maybe we can get this info from cellarea data
            mesh = cellarea.getGrid().getMesh()
            latitude_bounds = mesh[:,0]
            longitude_bounds = mesh[:,1]
            warnings.warn("You did not pass lat/lon bounds but we could infer them from cellarea")
        except:
            pass

    if longitude_bounds is None or latitude_bounds is None:
        raise RuntimeError("You did not pass lat/lon bounds and couldn't infer them from cellarea")


    # Save info for later
    if isinstance(cellarea, cdms2.avariable.AbstractVariable):
        orig_shape = cellarea.shape
        orig_axes = cellarea.getAxisList()

    latitude_bounds = degrees2radians(latitude_bounds)
    longitude_bounds = degrees2radians(longitude_bounds)

    # distance between successive corners
    sh = list(latitude_bounds.shape[:-1])
    del_lats = numpy.ma.zeros(sh)
    del_lons = numpy.ma.zeros(sh)
    max_distance = numpy.ma.zeros(sh)

    for i in range(sh[-1]):
        for j in range(i+1, sh[-1]):
            del_lats = latitude_bounds[:,i] - latitude_bounds[:,j] 
            del_lons = longitude_bounds[:,i] - longitude_bounds[:,j] 
            # formula from: https://en.wikipedia.org/wiki/Great-circle_distance
            distance = 2.* numpy.ma.asin(numpy.ma.sqrt(numpy.ma.sin(del_lats/2.)**2 + numpy.ma.cos(numpy.ma.latitude_bounds[:,i])*numpy.ma.cos(latitude_bounds[:,j])*numpy.ma.sin(del_lons/2.)**2))
            max_distance = numpy.ma.maximum(max_distance, distance)

    radius = 6371.  # in km
    accumlation = numpy.ma.sum(cellarea*max_distance) * radius / numpy.ma.sum(cellarea)
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





