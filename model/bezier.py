from PySide6.QtGui import QVector3D
from geometry.bezier import generate_vertices_grid
from geometry.general import rotate_by_Z_X

class Vertex:
    # def __init__(self, u: float, v: float, V: list[list[QVector3D]]):
    #     self.u = u
    #     self.v = v
    #     self.P, self.Pu, self.Pv, self.N = evaluate_bezier_point(u, v, V)
    #     # After rotation
    #     self.P_rot = self.P
    #     self.Pu_rot = self.Pu
    #     self.Pv_rot = self.Pv
    #     self.N_rot = self.N

    def __init__(self, u: float, v: float, P: QVector3D, Pu: QVector3D,
                 Pv: QVector3D, N: QVector3D):
        self.u = u
        self.v = v
        self.P = P
        self.Pu = Pu
        self.Pv = Pv
        self.N = N
        # After rotation
        self.P_rot = self.P
        self.Pu_rot = self.Pu
        self.Pv_rot = self.Pv
        self.N_rot = self.N

class ControlPoint:
    def __init__(self, x: float, y: float, z: float):
        self.original = QVector3D(x, y, z)
        # After rotation
        self.rot = self.original

class Triangle:
    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex):
        self.vertices = [v0, v1, v2]

class BezierSurface:
    def __init__(self, control_points: list[list[ControlPoint]]):
        self.control_points = control_points
        self.vertices_grid = []
        self.mesh = []
    
    def generate_mesh(self, divisions: int):
        # Generate grid of vertices
        self.vertices_grid = []
        u, v, P, Pu, Pv, N = generate_vertices_grid(self.control_points, divisions)
        for i in range(len(u)):
            row = []
            for j in range(len(v)):
                P_qvec = QVector3D(P[i][j][0], P[i][j][1], P[i][j][2])
                Pu_qvec = QVector3D(Pu[i][j][0], Pu[i][j][1], Pu[i][j][2])
                Pv_qvec = QVector3D(Pv[i][j][0], Pv[i][j][1], Pv[i][j][2])
                N_qvec = QVector3D(N[i][j][0], N[i][j][1], N[i][j][2])
                vertex = Vertex(u[i], v[j], P_qvec, Pu_qvec, Pv_qvec, N_qvec)
                row.append(vertex)
            self.vertices_grid.append(row)
        
        # Create triangles from the grid
        self.mesh = []
        for i in range(divisions):
            for j in range(divisions):
                # Get 4 vertices of the quad
                v00 = self.vertices_grid[i][j]
                v01 = self.vertices_grid[i][j + 1]
                v10 = self.vertices_grid[i + 1][j]
                v11 = self.vertices_grid[i + 1][j + 1]
                
                # Two triangles
                self.mesh.append(Triangle(v00, v01, v10))
                self.mesh.append(Triangle(v10, v11, v01))

    def rotate(self, alpha, beta):
        for row in self.vertices_grid:
            for v in row:
                v.P_rot = rotate_by_Z_X(v.P, alpha, beta)
                v.Pu_rot = rotate_by_Z_X(v.Pu, alpha, beta)
                v.Pv_rot = rotate_by_Z_X(v.Pv, alpha, beta)
                v.N_rot = rotate_by_Z_X(v.N, alpha, beta)
        for row in self.control_points:
            for cp in row:
                cp.rot = rotate_by_Z_X(cp.original, alpha, beta)

    def cpoints_original(self):
        return [[cp.original for cp in row] for row in self.control_points]
    
    def cpoints_rot(self):
        return [[cp.rot for cp in row] for row in self.control_points]