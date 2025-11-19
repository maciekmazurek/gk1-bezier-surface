from model.bezier import ControlPoint
from pathlib import Path
from PySide6.QtGui import QImage

def load_control_points(filename: str) -> list[list[ControlPoint]]:
    control_points = []

    with open(filename, 'r') as f:
        lines = f.readlines()

        if len(lines) != 16:
            raise ValueError("File must have exactly 16 lines")
        
        for i in range(4):
            row = []
            for j in range(4):
                line = lines[i * 4 + j].strip()
                x, y, z = map(float, line.split())
                row.append(ControlPoint(x, y, z))
            control_points.append(row)

    return control_points

def load_texture(texture_path: str) -> QImage:
    texture = QImage(texture_path)
    if texture.isNull():
        raise ValueError(f"[*] Failed to load image from {texture_path}")
    return texture

def get_path(relative_path: str) -> str:
    return str(Path(__file__).resolve().parent / relative_path)