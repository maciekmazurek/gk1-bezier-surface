from model.bezier import BezierSurface

import config

class BezierSurfaceGraphics:
    def __init__(self, control_points, texture, show_polygon, show_mesh, 
                 show_fill, normal_map, color=config.DEFAULT_SURFACE_COLOR):
        self.bezier_surface = BezierSurface(control_points)
        self.show_polygon = show_polygon
        self.show_mesh = show_mesh
        self.show_fill = show_fill
        self.color = color
        self.texture = texture
        self.texture_enabled = False
        self.normal_map = normal_map
        self.normal_mapping_enabled = False

    def rotate(self, alpha, beta):
        self.bezier_surface.rotate(alpha, beta)

    def generate_mesh(self, divisions):
        self.bezier_surface.generate_mesh(divisions)