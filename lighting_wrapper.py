import ctypes, numpy as np
from pathlib import Path
from PySide6.QtGui import QImage

class VertexC(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float),
        ("nx", ctypes.c_float), ("ny", ctypes.c_float), ("nz", ctypes.c_float),
        ("u", ctypes.c_float), ("v", ctypes.c_float),
        ("Pux", ctypes.c_float), ("Puy", ctypes.c_float), ("Puz", ctypes.c_float),
        ("Pvx", ctypes.c_float), ("Pvy", ctypes.c_float), ("Pvz", ctypes.c_float),
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

class TextureC(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("pixels", ctypes.POINTER(ctypes.c_uint32))
    ]

_lib = ctypes.CDLL(str(Path(__file__).parent / "lighting_c" / "lighting.dll"))
_lib.fill_surface.argtypes = [
    ctypes.POINTER(TriangleC), ctypes.c_int,
    ctypes.POINTER(LightingParamsC),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int,
    ctypes.POINTER(TextureC),
    ctypes.POINTER(TextureC)
]
_lib.fill_surface.restype = None
_lib.fill_surface_buffers = getattr(_lib, "fill_surface_buffers")
_lib.fill_surface_buffers.argtypes = [
    ctypes.POINTER(ctypes.c_float),  # positions
    ctypes.POINTER(ctypes.c_float),  # normals
    ctypes.POINTER(ctypes.c_float),  # pu
    ctypes.POINTER(ctypes.c_float),  # pv
    ctypes.POINTER(ctypes.c_float),  # uv
    ctypes.POINTER(ctypes.c_int),    # tri_indices
    ctypes.c_int,
    ctypes.POINTER(LightingParamsC),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int,
    ctypes.POINTER(TextureC), ctypes.POINTER(TextureC)
]
_lib.fill_surface_buffers.restype = None

def fill_surface_c(P_grid_rot, N_grid_rot, Pu_grid_rot, Pv_grid_rot,
                   u_grid, v_grid, tri_indices,
                   kd, ks, m, light_pos, io_color, il_color,
                   framebuffer: QImage, scale: float,
                   texture_qimage: QImage | None,
                   normal_map_qimage: QImage | None):
    # Flatten geometry to contiguous float32 buffers
    positions = (P_grid_rot.reshape(-1, 3) * scale).astype(np.float32, copy=False)
    normals   = N_grid_rot.reshape(-1, 3).astype(np.float32, copy=False)
    pu        = Pu_grid_rot.reshape(-1, 3).astype(np.float32, copy=False)
    pv        = Pv_grid_rot.reshape(-1, 3).astype(np.float32, copy=False)
    uv        = np.stack([u_grid.ravel(), v_grid.ravel()], axis=1).astype(np.float32, copy=False)
    tri_idx   = tri_indices.astype(np.int32, copy=False)

    params = LightingParamsC()
    params.kd = kd; params.ks = ks; params.m = m
    params.lx = light_pos.x() * scale; params.ly = light_pos.y() * scale; params.lz = light_pos.z() * scale
    params.io_r = io_color.redF(); params.io_g = io_color.greenF(); params.io_b = io_color.blueF()
    params.il_r = il_color.redF(); params.il_g = il_color.greenF(); params.il_b = il_color.blueF()

    assert framebuffer.format() in (QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied)
    fb_w, fb_h = framebuffer.width(), framebuffer.height()
    buf = framebuffer.bits()
    np_img = np.ndarray((fb_h, fb_w), dtype=np.uint32, buffer=buf)
    img_ptr = np_img.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
    off_x = fb_w // 2
    off_y = fb_h // 2

    texture_ptr = None
    if texture_qimage is not None:
        assert texture_qimage.format() in (QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied)
        tex_w, tex_h = texture_qimage.width(), texture_qimage.height()
        tbuf = texture_qimage.bits()
        np_texture = np.ndarray((tex_h, tex_w), dtype=np.uint32, buffer=tbuf)
        texture_c = TextureC()
        texture_c.width = tex_w
        texture_c.height = tex_h
        texture_c.pixels = np_texture.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        texture_ptr = ctypes.byref(texture_c)

    normal_map_ptr = None
    if normal_map_qimage is not None:
        assert normal_map_qimage.format() in (QImage.Format_ARGB32, QImage.Format_ARGB32_Premultiplied)
        nm_w, nm_h = normal_map_qimage.width(), normal_map_qimage.height()
        nm_buf = normal_map_qimage.bits()
        np_normal_map = np.ndarray((nm_h, nm_w), dtype=np.uint32, buffer=nm_buf)
        normal_map_c = TextureC()
        normal_map_c.width = nm_w
        normal_map_c.height = nm_h
        normal_map_c.pixels = np_normal_map.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        normal_map_ptr = ctypes.byref(normal_map_c)

    _lib.fill_surface_buffers(
        positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        normals.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        pu.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        pv.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        uv.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        tri_idx.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),
        tri_idx.shape[0],
        ctypes.byref(params),
        img_ptr, fb_w, fb_h, off_x, off_y,
        texture_ptr, normal_map_ptr
    )