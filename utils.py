from pathlib import Path
from PySide6.QtGui import QImage

import numpy as np

def load_control_points(file_path: str) -> np.ndarray:
    control_points = np.loadtxt(file_path, dtype=np.float32)
    if control_points.shape != (16, 3):
            raise ValueError("[*] File must have exactly 16 lines, " \
            "each with 3 float values (x y z)")
    control_points.resize((4, 4, 3))

    return control_points

def load_texture(file_path: str) -> QImage:
    texture = QImage(file_path)
    if texture.isNull():
        raise ValueError(f"[*] Failed to load image from {file_path}")
    return texture.convertToFormat(QImage.Format_ARGB32)

def get_path(relative_path: str) -> str:
    return str(Path(__file__).resolve().parent / relative_path)