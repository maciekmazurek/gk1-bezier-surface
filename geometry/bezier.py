from PySide6.QtGui import QVector3D

import numpy as np

B = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
], dtype=float)

def decompose_matrix(V: list[list[QVector3D]]) -> tuple[list[list[float]], 
                                                        list[list[float]], 
                                                        list[list[float]]]:
    Vx = []
    Vy = []
    Vz = []
    for row in V:
        Vx_row = []
        Vy_row = []
        Vz_row = []
        for v in row:
            Vx_row.append(v.x())
            Vy_row.append(v.y())
            Vz_row.append(v.z())
        Vx.append(Vx_row)
        Vy.append(Vy_row)
        Vz.append(Vz_row)
    
    return (Vx, Vy, Vz)

def evaluate_bezier_point(u: float, v: float, V: list[list[QVector3D]]):
    Vx, Vy, Vz = decompose_matrix(V)
    u_vector = np.array([u**3, u*u, u, 1], dtype=float)
    du_vector = np.array([3*u*u, 2*u, 1, 0], dtype=float)
    v_vector = np.array([v**3, v*v, v, 1], dtype=float)
    dv_vector = np.array([3*v*v, 2*v, 1, 0], dtype=float)

    u_B = u_vector @ B
    du_B = du_vector @ B
    Bt_v = B.T @ v_vector
    Bt_dv = B.T @ dv_vector

    P = QVector3D()
    Pu = QVector3D()
    Pv = QVector3D()

    P.setX(u_B @ Vx @ Bt_v)
    P.setY(u_B @ Vy @ Bt_v)
    P.setZ(u_B @ Vz @ Bt_v)

    Pu.setX(du_B @ Vx @ Bt_v)
    Pu.setY(du_B @ Vy @ Bt_v)
    Pu.setZ(du_B @ Vz @ Bt_v)

    Pv.setX(u_B @ Vx @ Bt_dv)
    Pv.setY(u_B @ Vy @ Bt_dv)
    Pv.setZ(u_B @ Vz @ Bt_dv)

    N = QVector3D.normal(Pu, Pv)

    return P, Pu, Pv, N
