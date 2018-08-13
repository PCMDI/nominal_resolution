from __future__ import print_function
import unittest
import numpy
import nominal_resolution

class MPASTest(unittest.TestCase):

    def testIt(self):
        radius = 6371.
        cellarea = numpy.array([1.,1.])
        blats= numpy.array([[-8.695716125630886, -8.743596230455271, -8.63516813909499, -8.47180192573253, -8.424977900462013, -8.532991604024021, -8.532991604024021], [83.0722451487354, 83.09827824557905, 83.24785526448542, 83.39810919356844, 83.37442734959542, 83.21842863955908, 83.21842863955908]])
        blons = numpy.array([[51.0650943464591, 51.21168642417699, 51.33863462019597, 51.30106434286725, 51.15568215435684, 51.028332877885546, 51.028332877885546], [123.28552104391477, 124.92199149446174, 125.46917766638191, 124.61458426939708, 122.93720368239897, 122.41045356078911, 122.41045356078911]])
        correct= numpy.array([35.959866777444184, 40.226179274733745])
        test_resolution, max_d = nominal_resolution.mean_resolution(cellarea, blats, blons, convertdeg2rad=True, returnMaxDistance=True )

        print("Test resol: {:g}".format(test_resolution))
        print("MAX:",max_d)

        self.assertTrue(numpy.allclose(max_d,correct))

