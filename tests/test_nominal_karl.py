from __future__ import print_function, division
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
        blons2 = numpy.ma.zeros((nlon*nlat, 5))
        blats2 = numpy.ma.zeros((nlon*nlat, 5))
        rg = range(nlon*nlat)
        blons2[:,0] = [n%nlon + dlon/2. for n in rg]
        blons2[:,1] = blons2[:,0]
        blons2[:,2] = numpy.ma.masked
        blons2[:,3] = [n%nlon - dlon/2. for n in rg]
        blons2[:,4] = blons2[:,3]

        blats2[:,0] = [-90. + (n//nlon)*dlat for n in rg]
        blats2[:,1] = [-90. + (n//nlon+1)*dlat for n in rg]
        blats2[:,2] = numpy.ma.masked
        blats2[:,3] = [-90. + (n//nlon+1)*dlat for n in rg]
        blats2[:,4] = blats2[:,0]

        cellarea2 = radius**2 * (blons2[:,0]-blons2[:,3])*numpy.pi/180. * (numpy.sin(numpy.pi*blats2[:,3]/180.) - numpy.sin(numpy.pi*blats2[:,0]/180.))
        for i in numpy.arange(1,nlat+1)*nlon-1:
            cellarea2[i] = numpy.ma.masked

        return cellarea2, blats2, blons2, dlon, dlat

    def doit(self, nlon, nlat, resolution):
        print("Testing:",nlon, nlat)
        radius = 6371.
        cellarea, blats, blons, dlon, dlat = self.generateGrid(nlon, nlat)
        correct_resolution = radius*(dlat*numpy.pi/180.)/2. * (1. + ((dlat**2+dlon**2)/(dlat*dlon))*numpy.arctan(dlon/dlat))

        print("Correct: {:g}".format(correct_resolution))

        convertdeg2rad = True
        test_resolution = nominal_resolution.mean_resolution(cellarea, blats, blons, convertdeg2rad)

        print("Test resol: {:g}".format(test_resolution))

        print("tol:",(test_resolution-correct_resolution)/correct_resolution)

        if nlon<5:
            rtol = .05
        elif nlon<25:
            rtol = .02
        else:
            rtol = 0.001
        print("rtol is:",rtol)
        self.assertTrue(numpy.allclose(correct_resolution,test_resolution,rtol))
        self.assertEqual(nominal_resolution.nominal_resolution(test_resolution),resolution)


    def testMultipleResolutions(self):
        self.doit(3,4,"10000 km")
        self.doit(4,3,"10000 km")
        self.doit(10,9,"5000 km")
        self.doit(18,90,"2500 km")
        self.doit(180,10,"2500 km")
        self.doit(24,30,"1000 km")
        self.doit(80,40,"500 km")
        self.doit(180,90,"250 km")
        self.doit(360,180,"100 km")
        self.doit(900,500,"50 km")
        self.doit(1800,900,"25 km")
        self.doit(3600,1800,"10 km")





