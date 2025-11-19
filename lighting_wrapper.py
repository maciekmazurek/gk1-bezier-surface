import ctypes, numpy as np
from pathlib import Path
from PySide6.QtGui import QImage

class VertexC(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float),
        ("nx", ctypes.c_float), ("ny", ctypes.c_float), ("nz", ctypes.c_float),
    ]

class TriangleC(ctypes.Structure):
    _fields_ = [("v", VertexC * 3)]

class LightingParamsC(ctypes.Structure):
    _fields_ = [
        ("kd", ctypes.c_float), ("ks", ctypes.c_float),
        ("m", ctypes.c_int),
        ("lx", ctypes.c_float), ("ly", ctypes.c_float), ("lz", ctypes.c_float),
        ("io_r", ctypes.c_float), ("io_g", ctypes.c_float), ("io_b", ctypes.c_float),
        ("il_r", ctypes.c_float), ("il_g", ctypes.c_float), ("il_b", ctypes.c_float),
    ]

_lib = ctypes.CDLL(str(Path(__file__).parent / "lighting_c" / "lighting.dll"))
_lib.fill_surface.argtypes = [
    ctypes.POINTER(TriangleC), ctypes.c_int,
    ctypes.POINTER(LightingParamsC),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int
]
_lib.fill_surface.restype = None

def fill_surface_c(triangles_list, kd, ks, m, light_pos, io_color, il_color,
                   framebuffer: QImage, scale: float):
    tri_count = len(triangles_list)
    TriArrayType = TriangleC * tri_count
    tri_array = TriArrayType()
    for i, tri in enumerate(triangles_list):
        for j, v in enumerate(tri.vertices):
            p = v.P_rot; n = v.N_rot
            tri_array[i].v[j].x = p.x() * scale
            tri_array[i].v[j].y = p.y() * scale
            tri_array[i].v[j].z = p.z()
            tri_array[i].v[j].nx = n.x()
            tri_array[i].v[j].ny = n.y()
            tri_array[i].v[j].nz = n.z()

    params = LightingParamsC()
    params.kd = kd; params.ks = ks; params.m = m
    params.lx = light_pos.x(); params.ly = light_pos.y(); params.lz = light_pos.z()
    params.io_r = io_color.redF(); params.io_g = io_color.greenF(); params.io_b = io_color.blueF()
    params.il_r = il_color.redF(); params.il_g = il_color.greenF(); params.il_b = il_color.blueF()

    assert framebuffer.format() in (QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied)
    W, H = framebuffer.width(), framebuffer.height()
    buf = framebuffer.bits()
    np_img = np.ndarray((H, W), dtype=np.uint32, buffer=buf)
    img_ptr = np_img.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))

    off_x = W // 2
    off_y = H // 2

    _lib.fill_surface(tri_array, tri_count, ctypes.byref(params),
                      img_ptr, W, H, off_x, off_y)
    