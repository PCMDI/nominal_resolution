from __future__ import print_function
import unittest
import numpy
import nominal_resolution

class KarlTest(unittest.TestCase):
    def setUp(self):
        nlon = 180
        nlat = 90
        nmax = nlon*nlat
        nv = 5

        dlon = 360./nlon
        dlat = 180./(nlat)

        blons = numpy.ma.zeros((nmax,nv))
        blats = numpy.ma.zeros((nmax,nv))
        cellarea = numpy.ma.zeros(nmax)

        radius = 6371.
        # Horrible way but don't want to think about it
        # just copying Karl's Fortran like pseudo code
        for ilat in range(nlat):
            for ilon in range(nlon):
                n = ilon + ilat*nlon
                for i in range(2):
                    blons[n,i] = ilon + dlon/2.
                    blats[n,i] = -90.+(ilat+i)*dlat
                    blons[n,i+3] = ilon - dlon/2.
                    blats[n,i+3] = -90. + (ilat-i+1)*dlat
                blons[:,2] = numpy.ma.masked
                blats[:,2] = numpy.ma.masked
                if ilon == nlon-1:
                    cellarea[n] = numpy.ma.masked
                else:
                    cellarea[n] = radius**2 * (blons[n,0]-blons[n,3])*numpy.pi/180. * (numpy.sin(numpy.pi*blats[n,3]/180.) - numpy.sin(numpy.pi*blats[n,0]/180.))

        print("BLATS:",blats[:10])
        print("BLATS:",blats[-10:])
        print("CELL:",cellarea[:5])
        self.cellarea = cellarea
        self.blats = blats
        self.blons = blons
        self.radius = radius
        self.dlat = dlat
        self.dlon = dlon

    def testMe(self):
        correct_resolution = self.radius*(self.dlat*numpy.pi/360.)/2. * (1. + ((self.dlat**2+self.dlon**2)/(self.dlat*self.dlon))*numpy.arctan(self.dlon/self.dlat))

        print("COrrect: {:g}".format(correct_resolution))

        test_resolution = nominal_resolution.mean_resolution(self.cellarea, self.blats, self.blons)

        print("Test resol: {:g}".format(test_resolution))

        self.assertEqual(nominal_resolution.nominal_resolution(test_resolution),"500 km")







