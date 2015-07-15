import numpy as np
import matplotlib.pyplot as plt
from matplotlib import widgets
from projection import Quaternion, project_points

class Cube:
    """Magic Cube Representation"""
    # define some attribues
    default_plastic_color = 'black'
    default_face_colors = ["w", "#ffcf00","#00008f", "#009f0f","#ff6f00", "#cf0000","gray", "none"]

    base_face = np.array([[1, 1, 1],
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
    base_sticker = np.array([[d1, d2, d3], 
                             [d2, d1, d3],
                             [-d2, d1, d3], 
                             [-d1, d2, d3],
                             [-d1, -d2, d3], 
                             [-d2, -d1, d3],
                             [d2, -d1, d3], 
                             [d1, -d2, d3],
                             [d1, d2, d3]], dtype=float)

    base_face_centroid = np.array([[0, 0, 1]])
    base_sticker_centroid = np.array([[0, 0, 1 + stickerthickness]])
