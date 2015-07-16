import numpy as Rubik_NUMPY
class GRAFICO_CUBO
 
    @classmethod
    def from_v_theta(cls, v, theta):
     
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

        return cls(x)

    def __init__(self, x):
        self.x = Rubik_NUMPY.asarray(x, dtype=float)

    def __repr__(self):
        return "GRAFICO_CUBO\n" + self.x.__repr__()

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

    def as_v_theta(self):
       
        x = self.x.reshape((-1, 4)).T

        # aki capturamos  la theta
        norm = Rubik_NUMPY.sqrt((x ** 2).sum(0))
        theta = 2 * Rubik_NUMPY.arccos(x[0] / norm)

        # capturando el vector
        v = Rubik_NUMPY.array(x[1:], order='F', copy=True)
        v /= Rubik_NUMPY.sqrt(Rubik_NUMPY.sum(v ** 2, 0))

        # remodelar los resultados
        v = v.T.reshape(self.x.shape[:-1] + (3,))
        theta = theta.reshape(self.x.shape[:-1])

        return v, theta

    def as_rotation_matrix(self):
        """devuelve la rotacion matriz (normalizado) quaternion"""
        v, theta = self.as_v_theta()

        shape = theta.shape
        theta = theta.reshape(-1)
        v = v.reshape(-1, 3).T
        c = Rubik_NUMPY.cos(theta)
        s = Rubik_NUMPY.sin(theta)

        mat = Rubik_NUMPY.array([[v[0] * v[0] * (1. - c) + c,
                         v[0] * v[1] * (1. - c) - v[2] * s,
                         v[0] * v[2] * (1. - c) + v[1] * s],
                        [v[1] * v[0] * (1. - c) + v[2] * s,
                         v[1] * v[1] * (1. - c) + c,
                         v[1] * v[2] * (1. - c) - v[0] * s],
                        [v[2] * v[0] * (1. - c) - v[1] * s,
                         v[2] * v[1] * (1. - c) + v[0] * s,
                         v[2] * v[2] * (1. - c) + c]],
                       order='F').T
        return mat.reshape(shape + (3, 3))

    def rotate(self, points):
        M = self.as_rotation_matrix()
        
        return Rubik_NUMPY.dot(points, M.T)


def project_points(points, q, view, vertical=[0, 1, 0]):
   
    points = Rubik_NUMPY.asarray(points)
    view = Rubik_NUMPY.asarray(view)

    xdir = Rubik_NUMPY.cross(vertical, view).astype(float)

    if Rubik_NUMPY.all(xdir == 0):
        raise ValueError("vertical is parallel to v")

    xdir /= Rubik_NUMPY.sqrt(Rubik_NUMPY.dot(xdir, xdir))

    # obtener vecto vertical
    ydir = Rubik_NUMPY.cross(view, xdir)
    ydir /= Rubik_NUMPY.sqrt(Rubik_NUMPY.dot(ydir, ydir))

    # normalizar la ubicacion en eje z
    v2 = Rubik_NUMPY.dot(view, view)
    zdir = view / Rubik_NUMPY.sqrt(v2)

    # rotar los puntos
    R = q.as_rotation_matrix()
    Rpts = Rubik_NUMPY.dot(points, R.T)

    # proyectar  los puntos en vista
    dpoint = Rpts - view
    dpoint_view = Rubik_NUMPY.dot(dpoint, view).reshape(dpoint.shape[:-1] + (1,))
    dproj = -dpoint * v2 / dpoint_view

    trans = range(1, dproj.ndim) + [0]
    return Rubik_NUMPY.array([Rubik_NUMPY.dot(dproj, xdir),
                     Rubik_NUMPY.dot(dproj, ydir),
                     -Rubik_NUMPY.dot(dpoint, zdir)]).transpose(trans)
