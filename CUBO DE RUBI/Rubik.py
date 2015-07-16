import numpy as Rubik_NUMPY
import matplotlib.pyplot as plt
from matplotlib import widgets
from projection import GRAFICO_CUBO, project_points

class Cube:
    """Magic Cube Representation"""
    # define some attribues
    color_defecto = 'black'
    color_de_cara = ["w", "#ffcf00","#00008f", "#009f0f","#ff6f00", "#cf0000","gray", "none"]

    base_face = Rubik_NUMPY.array([[1, 1, 1],
                          [1, -1, 1],
                          [-1, -1, 1],
                          [-1, 1, 1],
                          [1, 1, 1]], dtype=float)
    ancho_etiqueta = 0.9
    margen_etiqueta = 0.5 * (1. - ancho_etiqueta)
    espesor_etiqueta = 0.001
    (d1, d2, d3) = (1 - margen_etiqueta,
                    1 - 2 * margen_etiqueta,
                    1 + espesor_etiqueta)
    base_sticker = Rubik_NUMPY.array([[d1, d2, d3], 
                             [d2, d1, d3],
                             [-d2, d1, d3], 
                             [-d1, d2, d3],
                             [-d1, -d2, d3], 
                             [-d2, -d1, d3],
                             [d2, -d1, d3], 
                             [d1, -d2, d3],
                             [d1, d2, d3]], dtype=float)

    cara_base_central = Rubik_NUMPY.array([[0, 0, 1]])
    base_central_ad = Rubik_NUMPY.array([[0, 0, 1 + espesor_etiqueta]])

    # Define rotation angles and axes for the six sides of the cube
    x, y, z = Rubik_NUMPY.eye(3)
    rots = [GRAFICO_CUBO.from_v_theta(x, theta)
            for theta in (Rubik_NUMPY.pi / 2, -Rubik_NUMPY.pi / 2)]
    rots += [GRAFICO_CUBO.from_v_theta(y, theta)
             for theta in (Rubik_NUMPY.pi / 2, -Rubik_NUMPY.pi / 2, Rubik_NUMPY.pi, 2 * Rubik_NUMPY.pi)]

    # define face movements
 

    def __init__(self, N=3, plastic_color=None, face_colors=None):
        self.N = N
        if plastic_color is None:
            self.plastic_color = self.color_defecto
        else:
            self.plastic_color = plastic_color

        if face_colors is None:
            self.face_colors = self.color_de_cara
        else:
            self.face_colors = face_colors

        self._move_list = []
        self._initialize_arrays()

    def _initialize_arrays(self):
  
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

            face_centroids_t = Rubik_NUMPY.dot(self.cara_base_central
                                      + translations, M.T)

            sticker_centroids_t = Rubik_NUMPY.dot(self.base_central_ad
                                         + translations, M.T)

            colors_i = i + Rubik_NUMPY.zeros(face_centroids_t.shape[0], dtype=int)

            # append face ID to the face centroids for lex-sorting
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

    