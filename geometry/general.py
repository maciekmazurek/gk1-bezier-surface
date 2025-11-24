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

def rotate_by_Z_X(vectors, alpha, beta):
    # vectors' shape is (..., 3)
    Rz = np_rotation_matrix_z(alpha)
    Rx = np_rotation_matrix_x(beta)
    R = Rx @ Rz
    return vectors @ R.T 

def position_on_circle(radius: float, angle: float):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return (x, y)