import numpy as Rubik_NUMPY
import matplotlib.pyplot as plt
from matplotlib import widgets
from Juego import GRAFICO_CUBO, Puntos_grafico


class Funcion_teclas(plt.Axes):
    def __init__(self, cube=None,
                 interactive=True,
                 view=(0, 0, 10),
                 fig=None, rect=[0, 0.16, 1, 0.84],
                 **kwargs):
        if cube is None:
            self.cube = Cube(3)
        elif isinstance(cube, Cube):
            self.cube = cube
        else:
            self.cube = Cube(cube)

        self._view = view
        self._start_rot = GRAFICO_CUBO.from_v_theta((1, -1, 0),-Rubik_NUMPY.pi / 6)

        if fig is None:
            fig = plt.gcf()
            callbacks = fig.canvas.callbacks.callbacks
        del callbacks['key para eventos']
        kwargs.update(dict(aspect=kwargs.get('aspect', 'equal'),
                           xlim=kwargs.get('xlim', (-2.0, 2.0)),
                           ylim=kwargs.get('ylim', (-2.0, 2.0)),
                           frameon=kwargs.get('frameon', False),
                           xticks=kwargs.get('xticks', []),
                           yticks=kwargs.get('yticks', [])))
        super(InteractiveCube, self).__init__(fig, rect, **kwargs)
        self.xaxis.set_major_formatter(plt.NullFormatter())
        self.yaxis.set_major_formatter(plt.NullFormatter())

        self._start_xlim = kwargs['xlim']
        self._start_ylim = kwargs['ylim']
        self._ax_UD = (1, 0, 0)
        self._step_UD = 0.01
        self._ax_LR = (0, -1, 0)
        self._step_LR = 0.01
        self._ax_LR_alt = (0, 0, 1)

        self._active = False
        self._button1 = False
        self._button2 = False
        self._event_xy = None
        self._shift = False
        self._digit_flags = Rubik_NUMPY.zeros(10, dtype=bool)

        self._current_rot = self._start_rot
        self._face_polys = None
        self._sticker_polys = None

        self._draw_cube()

        
        self.figure.canvas.mpl_connect('precione la tecla de direccion',
                                       self._mouse_press)
        self.figure.canvas.mpl_connect('precione la tecla de direccion',
                                       self._mouse_release)
        self.figure.canvas.mpl_connect('precione la tecla de direccion',
                                       self._mouse_motion)
        self.figure.canvas.mpl_connect('precione la tecla de direccion',
                                       self._key_press)
        self.figure.canvas.mpl_connect('precione la tecla de direccion',
                                       self._key_release)
        plt.title('CUBO DE RUBIK')
 
    def _project(self, pts):
        return Puntos_grafico(pts, self._current_rot, self._view, [0, 1, 0])

    def _draw_cube(self):
        stickers = self._project(self.cube._stickers)[:, :, :2]
        faces = self._project(self.cube._faces)[:, :, :2]
        face_centroids = self._project(self.cube._face_centroids[:, :3])
        sticker_centroids = self._project(self.cube._sticker_centroids[:, :3])

        plastic_color = self.cube.plastic_color
        colors = Rubik_NUMPY.asarray(self.cube.face_colors)[self.cube._colors]
        face_zorders = -face_centroids[:, 2]
        sticker_zorders = -sticker_centroids[:, 2]

        if self._face_polys is None:
            self._face_polys = []
            self._sticker_polys = []

            for i in range(len(colors)):
                fp = plt.Polygon(faces[i], facecolor=plastic_color,
                                 zorder=face_zorders[i])
                sp = plt.Polygon(stickers[i], facecolor=colors[i],
                                 zorder=sticker_zorders[i])

                self._face_polys.append(fp)
                self._sticker_polys.append(sp)
                self.add_patch(fp)
                self.add_patch(sp)
        else:
            for i in range(len(colors)):
                self._face_polys[i].set_xy(faces[i])
                self._face_polys[i].set_zorder(face_zorders[i])
                self._face_polys[i].set_facecolor(plastic_color)

                self._sticker_polys[i].set_xy(stickers[i])
                self._sticker_polys[i].set_zorder(sticker_zorders[i])
                self._sticker_polys[i].set_facecolor(colors[i])

        self.figure.canvas.draw()

    def rotate(self, rot):
        self._current_rot = self._current_rot * rot

    def rotate_face(self, face, turns=1, layer=0, steps=5):
        if not Rubik_NUMPY.allclose(turns, 0):
            for i in range(steps):
                self.cube.rotate_face(face, turns * 1. / steps,
                                      layer=layer)
                self._draw_cube()

    def _reset_view(self, *args):
        self.set_xlim(self._start_xlim)
        self.set_ylim(self._start_ylim)
        self._current_rot = self._start_rot
        self._draw_cube()

    def _solve_cube(self, *args):
        move_list = self.cube._move_list[:]
        for (face, n, layer) in move_list[::-1]:
            self.rotate_face(face, -n, layer, steps=3)
        self.cube._move_list = []

    def _key_press(self, event):
        if event.key == 'shift':
            self._shift = True
        elif event.key.isdigit():
            self._digit_flags[int(event.key)] = 1
        elif event.key == 'right':
            if self._shift:
                ax_LR = self._ax_LR_alt
            else:
                ax_LR = self._ax_LR
            self.rotate(GRAFICO_CUBO.from_v_theta(ax_LR,
                                                5 * self._step_LR))
        elif event.key == 'left':
            if self._shift:
                ax_LR = self._ax_LR_alt
            else:
                ax_LR = self._ax_LR
            self.rotate(GRAFICO_CUBO.from_v_theta(ax_LR,
                                                -5 * self._step_LR))
        elif event.key == 'up':
            self.rotate(GRAFICO_CUBO.from_v_theta(self._ax_UD,
                                                5 * self._step_UD))
        elif event.key == 'down':
            self.rotate(GRAFICO_CUBO.from_v_theta(self._ax_UD,
                                                -5 * self._step_UD))
        elif event.key.upper() in 'RUDBLF':
            if self._shift:
                direction = -1
            else:
                direction = 1

            if Rubik_NUMPY.any(self._digit_flags[:N]):
                for d in Rubik_NUMPY.arange(N)[self._digit_flags[:N]]:
                    self.rotate_face(event.key.upper(), direction, layer=d)
            else:
                self.rotate_face(event.key.upper(), direction)
                self._draw_cube()

    def _key_release(self, event):
        if event.key == 'shift':
            self._shift = False
        elif event.key.isdigit():
            self._digit_flags[int(event.key)] = 0

    def _mouse_press(self, event):
        self._event_xy = (event.x, event.y)
        if event.button == 1:
            self._button1 = True
        elif event.button == 3:
            self._button2 = True

    def _mouse_release(self, event):
        self._event_xy = None
        if event.button == 1:
            self._button1 = False
        elif event.button == 3:
            self._button2 = False

    def _mouse_motion(self, event):
        """ giro con mauus"""

if __name__ == '__main__':
    import sys
    try:
        N = int(sys.argv[1])
    except:
        N = 2
    c = Cube(N)
    c.draw_interactive()
    plt.show()
