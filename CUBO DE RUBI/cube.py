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

    xdirs = [Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([1., 0., 0.]),
               Rubik_NUMPY.array([-1., 0., 0.]),
               Rubik_NUMPY.array([0., 0., -1.]),
               Rubik_NUMPY.array([0, 0., 1.])]

    colordict = {"w":0, "y":1, "b":2, "g":3, "o":4, "r":5}

    pltpos = [(0., 1.05), (0., -1.05), (0., 0.), (2.10, 0.), (1.05, 0.), (-1.05, 0.)]
    labelcolor = "#7f00ff"
    def __init__(self, N, whiteplastic=False):
     
        self.N = N
        self.stickers = Rubik_NUMPY.array([Rubik_NUMPY.tile(i, (self.N, self.N)) for i in range(6)])
        self.stickercolors = ["w", "#ffcf00", "#00008f", "#009f0f", "#ff6f00", "#cf0000"]
        self.stickerthickness = 0.001 
        self.stickerwidth = 0.9 
        if whiteplastic:
            self.plasticcolor = "#dfdfdf"
        else:
            self.plasticcolor = "#1f1f1f"
        self.fontsize = 12. * (self.N / 5.)
        return None

    def turn(self, f, d):
     
        for l in range(self.N):
            self.move(f, l, d)
        return None

    def move(self, f, l, d):
    
        i = self.facedict[f]
        l2 = self.N - 1 - l
        assert l < self.N
        ds = range((d + 4) % 4)
        if f == "U":
            f2 = "D"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["F"], range(self.N), l2),
                              (self.facedict["R"], range(self.N), l2),
                              (self.facedict["B"], range(self.N), l2),
                              (self.facedict["L"], range(self.N), l2)])
        if f == "D":
            return self.move("U", l2, -d)
        if f == "F":
            f2 = "B"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], range(self.N), l),
                              (self.facedict["L"], l2, range(self.N)),
                              (self.facedict["D"], range(self.N)[::-1], l2),
                              (self.facedict["R"], l, range(self.N)[::-1])])
        if f == "B":
            return self.move("F", l2, -d)
        if f == "R":
            f2 = "L"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], l2, range(self.N)),
                              (self.facedict["F"], l2, range(self.N)),
                              (self.facedict["D"], l2, range(self.N)),
                              (self.facedict["B"], l, range(self.N)[::-1])])
        if f == "L":
            return self.move("R", l2, -d)
        for d in ds:
            if l == 0:
                self.stickers[i] = Rubik_NUMPY.rot90(self.stickers[i], 3)
            if l == self.N - 1:
                self.stickers[i2] = Rubik_NUMPY.rot90(self.stickers[i2], 1)
        print "moved", f, l, len(ds)
        return None
