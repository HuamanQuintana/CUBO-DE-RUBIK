import numpy as Rubik_NUMPY
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

class Cube(object):

    facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}
    dictface = dict([(v, k) for k, v in facedict.items()])
    normals = [Rubik_NUMPY.array([0., 1., 0.]),
               Rubik_NUMPY.array([0., -1., 0.]),
               Rubik_NUMPY.array([0., 0., 1.]),
               Rubik_NUMPY.array([0., 0., -1.]),
               Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([-1., 0., 0.])]

    # this xdirs has to be synchronized with the self.move() function
    xdirs = [Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([-1., 0., 0.]),
               Rubik_NUMPY.array([0., 0., -1.]),
               Rubik_NUMPY.array([0, 0., 1.])]

    colordict = {"w":0, "y":1, "b":2, "g":3, "o":4, "r":5}

    pltpos = [(0., 1.05), (0., -1.05), (0., 0.), (2.10, 0.), (1.05, 0.), (-1.05, 0.)]
    labelcolor = "#7f00ff"
