from PySide6.QtGui import QVector3D

def load_control_points(filename: str) -> list[list[QVector3D]]:
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
                row.append(QVector3D(x, y, z))
            control_points.append(row)

    return control_points