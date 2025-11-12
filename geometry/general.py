from PySide6.QtGui import QVector3D

import numpy as np
import math

def np_rotation_matrix_z(angle_deg):
    """Numpy rotation matrix around the Z axis"""
    angle = math.radians(angle_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    return np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ], dtype=float)

def np_rotation_matrix_x(angle_deg):
    """Numpy rotation matrix around the X axis"""
    angle = math.radians(angle_deg)
    cos_b = math.cos(angle)
    sin_b = math.sin(angle)
    
    return np.array([
        [1,     0,      0],
        [0, cos_b, -sin_b],
        [0, sin_b,  cos_b]
    ], dtype=float)

def rotate_by_Z_X(vector, alpha, beta):
    """Rotate a Qt QVector3D by alpha degrees around Z, then beta degrees around X.

    The function converts the Qt vector to numpy, applies Z then X rotation matrices,
    and converts the result back to QVector3D.
    """
    np_matrix_z = np_rotation_matrix_z(alpha)
    np_matrix_x = np_rotation_matrix_x(beta)

    return np_to_qt(np_matrix_x @ np_matrix_z @ qt_to_np(vector))

def np_to_qt(vector):
    return QVector3D(vector[0], vector[1], vector[2])

def qt_to_np(vector: QVector3D):
    return np.array([vector.x(), vector.y(), vector.z()], dtype=float)
