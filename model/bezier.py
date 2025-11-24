from geometry.bezier import generate_vertices_grid
from geometry.general import rotate_by_Z_X

import numpy as np

class BezierSurface:
    def __init__(self, control_points: np.ndarray):
        self.cp_grid = control_points
        self.cp_grid_rot = self.cp_grid.copy()
        # Mesh params
        self.u_grid = None
        self.v_grid = None
        self.P_grid = None
        self.Pu_grid = None
        self.Pv_grid = None
        self.N_grid = None
        self.P_grid_rot = None
        self.Pu_grid_rot = None
        self.Pv_grid_rot = None
        self.N_grid_rot = None
        self.tri_indices = None
    
    def generate_mesh(self, divisions: int):
        # Generate grid of vertices
        self.u_grid, self.v_grid, self.P_grid, self.Pu_grid, self.Pv_grid, self.N_grid = generate_vertices_grid(self.cp_grid, divisions)
        self.P_grid_rot = self.P_grid.copy()
        self.Pu_grid_rot = self.Pu_grid.copy()
        self.Pv_grid_rot = self.Pv_grid.copy()
        self.N_grid_rot = self.N_grid.copy()
        # Create triangles from the grid
        self.tri_indices = build_triangle_indices(divisions)

    def rotate(self, alpha, beta):
        self.P_grid_rot = rotate_by_Z_X(self.P_grid, alpha, beta)
        self.Pu_grid_rot = rotate_by_Z_X(self.Pu_grid, alpha, beta)
        self.Pv_grid_rot = rotate_by_Z_X(self.Pv_grid, alpha, beta)
        self.N_grid_rot = rotate_by_Z_X(self.N_grid, alpha, beta)
        self.cp_grid_rot = rotate_by_Z_X(self.cp_grid, alpha, beta)

def build_triangle_indices(divisions: int) -> np.ndarray:
    # Liczba wierzchołków w jednym wymiarze
    n = divisions + 1
    # Indeksy w siatce (n x n)
    idx = np.arange(n*n, dtype=np.int32).reshape(n, n)

    # Siatka kwadratów (divisions x divisions)
    I, J = np.meshgrid(np.arange(divisions), np.arange(divisions), indexing='ij')

    # Wierzchołki kwadratu
    v00 = idx[I, J]
    v01 = idx[I, J + 1]
    v10 = idx[I + 1, J]
    v11 = idx[I + 1, J + 1]

    # Dwa trójkąty na kwadrat
    tri1 = np.stack([v00, v01, v10], axis=-1)  # (divisions, divisions, 3)
    tri2 = np.stack([v10, v11, v01], axis=-1)

    # Spłaszczenie do (2*divisions*divisions, 3)
    tri_indices = np.concatenate(
        [tri1.reshape(-1, 3), tri2.reshape(-1, 3)],
        axis=0
    )
    return tri_indices