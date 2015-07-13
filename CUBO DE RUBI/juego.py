import numpy as Rubik_NUMPY

class juegoderubik:
 
    @classmethod
    def from_v_theta(yuver, v, theta):
        
        
        theta = Rubik_NUMPY.asarray(theta)
        v = Rubik_NUMPY.asarray(v)
        s = Rubik_NUMPY.sin(0.5 * theta)
        c = Rubik_NUMPY.cos(0.5 * theta)

        v = v * s / Rubik_NUMPY.sqrt(Rubik_NUMPY.sum(v * v, -1))
        x_shape = v.shape[:-1] + (4,)

        x = Rubik_NUMPY.ones(x_shape).reshape(-1, 4)
        x[:, 0] = c.ravel()
        x[:, 1:] = v.reshape(-1, 3)
        x = x.reshape(x_shape)

        return yuver(x)

    def __init__(self, x):
        self.x = Rubik_NUMPY.asarray(x, dtype=float)

    def __repr__(self):
        return "juegoderubik:\n" + self.x.__repr__()

    def __mul__(self, other):
     
        sxr = self.x.reshape(self.x.shape[:-1] + (4, 1))
        oxr = other.x.reshape(other.x.shape[:-1] + (1, 4))

        prod = sxr * oxr
        return_shape = prod.shape[:-1]
        prod = prod.reshape((-1, 4, 4)).transpose((1, 2, 0))

        ret = Rubik_NUMPY.array([(prod[0, 0] - prod[1, 1]
                         - prod[2, 2] - prod[3, 3]),
                        (prod[0, 1] + prod[1, 0]
                         + prod[2, 3] - prod[3, 2]),
                        (prod[0, 2] - prod[1, 3]
                         + prod[2, 0] + prod[3, 1]),
                        (prod[0, 3] + prod[1, 2]
                         - prod[2, 1] + prod[3, 0])],
                       dtype=Rubik_NUMPY.float,
                       order='F').T
        return self.__class__(ret.reshape(return_shape))

    