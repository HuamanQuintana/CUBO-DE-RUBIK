import numpy as Rubik_NUMPY
import matplotlib.pyplot as plt
from matplotlib import widgets
from Juego import GRAFICO_CUBO, Puntos_grafico
from F_Teclas import Funcion_teclas

class Cube:
# definicion de colores y atributos
    default_plastic_color = 'black'
    default_face_colors = ["w", "#ffcf00","#00008f", "#009f0f","#ff6f00", "#cf0000","gray", "none"]
    base_face = Rubik_NUMPY.array(
                          [[1, 1, 1],
                          [1, -1, 1],
                          [-1, -1, 1],
                          [-1, 1, 1],
                          [1, 1, 1]], dtype=float)
    stickerwidth = 0.9
    stickermargin = 0.5 * (1. - stickerwidth)
    stickerthickness = 0.001
    (d1, d2, d3) = (1 - stickermargin,
                    1 - 2 * stickermargin,
                    1 + stickerthickness)
    base_sticker = Rubik_NUMPY.array([[d1, d2, d3], [d2, d1, d3],
                             [-d2, d1, d3], [-d1, d2, d3],
                             [-d1, -d2, d3], [-d2, -d1, d3],
                             [d2, -d1, d3], [d1, -d2, d3],
                             [d1, d2, d3]], dtype=float)

    base_face_centroid = Rubik_NUMPY.array([[0, 0, 1]])
    base_sticker_centroid = Rubik_NUMPY.array([[0, 0, 1 + stickerthickness]])
    # definicion de angulos de rotacion para los 6 lados del cubo
    x, y, z = Rubik_NUMPY.eye(3)
    rots = [GRAFICO_CUBO.from_v_theta(x, theta)
            for theta in (Rubik_NUMPY.pi / 2, -Rubik_NUMPY.pi / 2)]
    rots += [GRAFICO_CUBO.from_v_theta(y, theta)
             for theta in (Rubik_NUMPY.pi / 2, -Rubik_NUMPY.pi / 2, Rubik_NUMPY.pi, 2 * Rubik_NUMPY.pi)]
    facesdict = dict(F=z, B=-z,R=x, L=-x,U=y, D=-y)
 # definicion de movimiento de caras del cubo
 
    def __init__(self, N=2, plastic_color=None, face_colors=None):
        self.N = N
        if plastic_color is None:
            self.plastic_color = self.default_plastic_color
        else:
            self.plastic_color = plastic_color

        if face_colors is None:
            self.face_colors = self.default_face_colors
        else:
            self.face_colors = face_colors

        self._move_list = []
        self._initialize_arrays()

    def _initialize_arrays(self):
        cubie_width = 2. / self.N
        translations = Rubik_NUMPY.array([[[-1 + (i + 0.5) * cubie_width,
                                   -1 + (j + 0.5) * cubie_width, 0]]
                                 for i in range(self.N)
                                 for j in range(self.N)])
        face_centroids = []
        faces = []
        sticker_centroids = []
        stickers = []
        colors = []

        factor = Rubik_NUMPY.array([1. / self.N, 1. / self.N, 1])

        for i in range(6):
            M = self.rots[i].as_rotation_matrix()
            faces_t = Rubik_NUMPY.dot(factor * self.base_face
                             + translations, M.T)
            stickers_t = Rubik_NUMPY.dot(factor * self.base_sticker
                                + translations, M.T)
            face_centroids_t = Rubik_NUMPY.dot(self.base_face_centroid
                                      + translations, M.T)
            sticker_centroids_t = Rubik_NUMPY.dot(self.base_sticker_centroid
                                         + translations, M.T)
            colors_i = i + Rubik_NUMPY.zeros(face_centroids_t.shape[0], dtype=int)
            face_centroids_t = Rubik_NUMPY.hstack([face_centroids_t.reshape(-1, 3),
                                          colors_i[:, None]])
            sticker_centroids_t = sticker_centroids_t.reshape((-1, 3))

            faces.append(faces_t)
            face_centroids.append(face_centroids_t)
            stickers.append(stickers_t)
            sticker_centroids.append(sticker_centroids_t)
            colors.append(colors_i)

        self._face_centroids = Rubik_NUMPY.vstack(face_centroids)
        self._faces = Rubik_NUMPY.vstack(faces)
        self._sticker_centroids = Rubik_NUMPY.vstack(sticker_centroids)
        self._stickers = Rubik_NUMPY.vstack(stickers)
        self._colors = Rubik_NUMPY.concatenate(colors)

        self._sort_faces()

    def _sort_faces(self):
        ind = Rubik_NUMPY.lexsort(self._face_centroids.T)
        self._face_centroids = self._face_centroids[ind]
        self._sticker_centroids = self._sticker_centroids[ind]
        self._stickers = self._stickers[ind]
        self._colors = self._colors[ind]
        self._faces = self._faces[ind]

    def rotate_face(self, f, n=1, layer=0):
        if layer < 0 or layer >= self.N:
            raise ValueError(' ')

        try:
            f_last, n_last, layer_last = self._move_list[-1]
        except:
            f_last, n_last, layer_last = None, None, None

        if (f == f_last) and (layer == layer_last):
            ntot = (n_last + n) % 4
            if abs(ntot - 4) < abs(ntot):
                ntot = ntot - 4
            if Rubik_NUMPY.allclose(ntot, 0):
                self._move_list = self._move_list[:-1]
            else:
                self._move_list[-1] = (f, ntot, layer)
        else:
            self._move_list.append((f, n, layer))
        
        v = self.facesdict[f]
        r = GRAFICO_CUBO.from_v_theta(v, n * Rubik_NUMPY.pi / 2)
        M = r.as_rotation_matrix()

        proj = Rubik_NUMPY.dot(self._face_centroids[:, :3], v)
        cubie_width = 2. / self.N
        flag = ((proj > 0.9 - (layer + 1) * cubie_width) &
                (proj < 1.1 - layer * cubie_width))

        for x in [self._stickers, self._sticker_centroids,
                  self._faces]:
            x[flag] = Rubik_NUMPY.dot(x[flag], M.T)
        self._face_centroids[flag, :3] = Rubik_NUMPY.dot(self._face_centroids[flag, :3],
                                                M.T)

    def draw_interactive(self):
        fig = plt.figure(figsize=(10, 10))
        fig.add_axes(Funcion_teclas(self))
        return fig
