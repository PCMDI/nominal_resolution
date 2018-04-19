import numpy, numpy.ma
import cdms2
import warnings

def degrees2radians(data, force=False):
    """Converts data from deg to radians"""
    if data.max > 7. or force:
        data = data / 180. * numpy.pi
    return data


def compute_nominal_resolution(cellarea, longitude_bounds=None, latitude_bounds=None):
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

    # some constants and variables for calculations
    radius = 6371.  # in km
    accum = 0.
    totarea = 0.

    # distance between successive corners
    sh = list(latitude_bounds.shape[:-1])
    del_lats = numpy.ma.zeros(sh)
    del_lons = numpy.ma.zeros(sh)
    max_distance = numpy.ma.zeros(sh)

    for i in range(sh[-1]):
        for j in range(i+1, sh[-1]):
            del_lats = latitude_bounds[:,i] - latitude_bounds[:,j] 
            del_lons = longitude_bounds[:,i] - longitude_bounds[:,j] 
            distance = 2.* numpy.ma.asin(numpy.ma.sqrt(numpy.ma.sin(del_lats/2.)**2 + numpy.ma.cos(numpy.ma.latitude_bounds[:,i]*numpy.ma.cos(latitude_bounds[:,j]* numpy.ma.sin(del_lons/2.)**2) 
