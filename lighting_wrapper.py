import ctypes
import numpy as np
from pathlib import Path
from PySide6.QtGui import QImage

_lib_path = Path(__file__).parent / "lighting_c" / "lighting.dll"
_lib = ctypes.CDLL(str(_lib_path))

_lib.fill_surface.argtypes = [
    ctypes.POINTER(ctypes.c_float),  # triangles
    ctypes.c_int,                    # tri_count
    ctypes.c_float,                  # kd
    ctypes.c_float,                  # ks
    ctypes.c_int,                    # m
    ctypes.c_float, ctypes.c_float, ctypes.c_float,  # lx, ly, lz
    ctypes.c_float, ctypes.c_float, ctypes.c_float,  # io_r, io_g, io_b
    ctypes.c_float, ctypes.c_float, ctypes.c_float,  # il_r, il_g, il_b
    ctypes.POINTER(ctypes.c_uint32), # img_ptr
    ctypes.c_int, ctypes.c_int,      # img_w, img_h
    ctypes.c_int, ctypes.c_int,      # offset_x, offset_y
]
_lib.fill_surface.restype = None

def fill_surface_c(triangles_list, kd, ks, m, light_pos, io_color, il_color,
                   framebuffer: QImage, scale: float):
    """
    triangles_list: lista trójkątów (każdy to 3 wierzchołki Vertex)
    kd, ks, m: parametry oświetlenia
    light_pos: QVector3D pozycji światła
    io_color, il_color: QColor obiekt/światło
    framebuffer: QImage do wypełnienia
    """
    # 1) spłaszcz trójkąty i PRZESKALUJ x,y do przestrzeni ekranu
    tri_data = []
    for tri in triangles_list:
        for v in tri.vertices:
            p = v.P_rot
            n = v.N_rot
            tri_data.extend([p.x() * scale, p.y() * scale, p.z(),
                             n.x(), n.y(), n.z()])
    tri_array = np.asarray(tri_data, dtype=np.float32)
    tri_ptr_c = tri_array.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    tri_count = len(triangles_list)

    # 2) kolory i światło
    io_r, io_g, io_b = io_color.redF(), io_color.greenF(), io_color.blueF()
    il_r, il_g, il_b = il_color.redF(), il_color.greenF(), il_color.blueF()
    lx, ly, lz = light_pos.x(), light_pos.y(), light_pos.z()

    # 3) wskaźnik do bufora QImage bez kopiowania
    assert framebuffer.format() in (QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied)
    img_w, img_h = framebuffer.width(), framebuffer.height()
    buf = framebuffer.bits()             # memoryview
    # Uwaga: dla ARGB32 bytesPerLine == 4*width, więc możemy użyć (h, w)
    np_img = np.ndarray((img_h, img_w), dtype=np.uint32, buffer=buf)
    img_ptr_c = np_img.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))

    offset_x = img_w // 2
    offset_y = img_h // 2

    _lib.fill_surface(
        tri_ptr_c, tri_count,
        kd, ks, m,
        lx, ly, lz,
        io_r, io_g, io_b,
        il_r, il_g, il_b,
        img_ptr_c,
        img_w, img_h,
        offset_x, offset_y
    )