from __future__ import print_function
import unittest
import numpy
import nominal_resolution

class KarlTest(unittest.TestCase):
    def generateGrid(self, nlon, nlat):
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

        return cellarea, blats, blons, dlon, dlat

    def doit(self, nlon, nlat):
        print("Testing:",nlon, nlat)
        radius = 6371.
        cellarea, blats, blons, dlon, dlat = self.generateGrid(nlon, nlat)
        correct_resolution = radius*(dlat*numpy.pi/180.)/2. * (1. + ((dlat**2+dlon**2)/(dlat*dlon))*numpy.arctan(dlon/dlat))

        print("Correct: {:g}".format(correct_resolution))

        convertdeg2rad = True
        test_resolution = nominal_resolution.mean_resolution(cellarea, blats, blons, convertdeg2rad)

        print("Test resol: {:g}".format(test_resolution))

        print("rtol:",(test_resolution-correct_resolution)/correct_resolution)
        rtol = 0.001
        if nlon<5:
            rtol = .05
        elif nlon<20:
            rtol = .02
        self.assertTrue(numpy.allclose(correct_resolution,test_resolution,rtol))
        #self.assertEqual(nominal_resolution.nominal_resolution(test_resolution),"250 km")


    def testMultipleResolutions(self):
        self.doit(3,4)
        self.doit(4,3)
        self.doit(10,9)
        self.doit(360,180)
        self.doit(18,90)
        self.doit(180,10)
        self.doit(180,90)
        self.doit(1800,900)





