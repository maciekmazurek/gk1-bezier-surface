import numpy as np

B = np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 3, 0, 0],
    [1, 0, 0, 0]
], dtype=float)

def generate_vertices_grid(cp_grid, divisions):
    Vx = cp_grid[:, :, 0]
    Vy = cp_grid[:, :, 1]
    Vz = cp_grid[:, :, 2]
    BVxBt = B @ Vx @ B.T
    BVyBt = B @ Vy @ B.T
    BVzBt = B @ Vz @ B.T

    u = np.linspace(0.0, 1.0, divisions + 1)
    v = np.linspace(0.0, 1.0, divisions + 1)

    U = np.column_stack([u**3, u**2, u, np.ones_like(u)])
    V = np.vstack([v**3, v**2, v, np.ones_like(v)])
    dU = np.column_stack([3*u**2, 2*u, np.ones_like(u), np.zeros_like(u)])
    dV = np.vstack([3*v**2, 2*v, np.ones_like(v), np.zeros_like(v)])

    Px = U @ BVxBt @ V
    Py = U @ BVyBt @ V
    Pz = U @ BVzBt @ V
    P = np.stack([Px, Py, Pz], axis=2)

    Pux = dU @ BVxBt @ V
    Puy = dU @ BVyBt @ V
    Puz = dU @ BVzBt @ V
    Pu = np.stack([Pux, Puy, Puz], axis=2)

    Pvx = U @ BVxBt @ dV
    Pvy = U @ BVyBt @ dV
    Pvz = U @ BVzBt @ dV
    Pv = np.stack([Pvx, Pvy, Pvz], axis=2)

    N = np.cross(Pu, Pv, axis=2)
    norm = np.linalg.norm(N, axis=2, keepdims=True)
    N = N / (norm + 1e-12)

    u_grid, v_grid = np.meshgrid(u, v, indexing='ij')

    return (u_grid, v_grid, P, Pu, Pv, N)