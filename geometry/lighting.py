from PySide6.QtGui import QVector3D

import math

def cos_between_vectors(v1: QVector3D, v2: QVector3D):
    return QVector3D.dotProduct(v1, v2)

def barycentric(px, py, p0, p1, p2):
    x0, y0 = p0.x(), p0.y()
    x1, y1 = p1.x(), p1.y()
    x2, y2 = p2.x(), p2.y()

    denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)

    w0 = ((y1 - y2)*(px - x2) + (x2 - x1)*(py - y2)) / denom
    w1 = ((y2 - y0)*(px - x2) + (x0 - x2)*(py - y2)) / denom
    w2 = 1 - w0 - w1

    return w0, w1, w2

def interpolate_point_params(px, py, p0, p1, p2, v0, v1, v2):
    # Barycentric coordinates of point (px, py) inside the triangle (p0, p1, p2)
    w0, w1, w2 = barycentric(px, py, p0, p1, p2)
    # Interpolated normal and z-coordinate
    N = w0*v0.N_rot + w1*v1.N_rot + w2*v2.N_rot
    z = w0*v0.P_rot.z() + w1*v1.P_rot.z() + w2*v2.P_rot.z()

    return (N, z)

def position_on_circle(radius: float, angle: float):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return (x, y)