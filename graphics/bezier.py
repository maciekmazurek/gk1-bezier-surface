from model.bezier import BezierSurface

import config

class BezierSurfaceGraphics:
    def __init__(self, control_points, texture, show_polygon, show_mesh, show_fill, color=config.DEFAULT_SURFACE_COLOR):
        self.bezier_surface = BezierSurface(control_points)
        self.show_polygon = show_polygon
        self.show_mesh = show_mesh
        self.show_fill = show_fill
        self.texture = texture
        self.color = color
        self.texture_enabled = True

    def rotate(self, alpha, beta):
        self.bezier_surface.rotate(alpha, beta)

    def generate_mesh(self, divisions):
        self.bezier_surface.generate_mesh(divisions)