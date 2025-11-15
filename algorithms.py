from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
import math

EPSILON = 1e-6

def scanline_filling(P: list[QPointF]) -> list[tuple[int, int]]:
    def update_AET(curr_idx: int, prev_idx: int, next_idx: int, P: list[QPointF], AET: dict):
        # Updating previous edge
        if P[prev_idx].y() >= P[curr_idx].y():
            prev_edge = eval_AET_edge(P[prev_idx], P[curr_idx], y)
            if prev_edge is not None:
                AET[(prev_idx, curr_idx)] = prev_edge
        else:
            AET.pop((prev_idx, curr_idx), None)

        # Updating next edge
        if P[next_idx].y() >= P[curr_idx].y():
            next_edge = eval_AET_edge(P[curr_idx], P[next_idx], y)
            if next_edge is not None:
                AET[(curr_idx, next_idx)] = next_edge
        else:
            AET.pop((curr_idx, next_idx), None)
        
    def eval_AET_edge(p0: QPointF, p1: QPointF, scan_line: float):
        # Ignore horizontal or nearly horizontal edges
        if abs(p1.y() - p0.y()) < EPSILON:
            return None
        
        # Ensure p_lower has smaller y (or equal y but smaller x)
        if (p0.y(), p0.x()) < (p1.y(), p1.x()):
            p_lower, p_upper = p0, p1
        else:
            p_lower, p_upper = p1, p0

        # Use half-open interval on Y: include lower y, exclude upper y
        if scan_line < p_lower.y() or scan_line >= p_upper.y():
            return None

        dx = p_upper.x() - p_lower.x()
        dy = p_upper.y() - p_lower.y()
        inv_m = dx / dy # 1 / m
        x_intersection = p_lower.x() + (scan_line - p_lower.y()) * inv_m

        return {
            'x': x_intersection,
            'inv_m': inv_m
        }

    def fill(x_values: list[int], y: int, pixels_filled: list):
        for i in range(0, len(x_values), 2):
            x0 = x_values[i]
            x1 = x_values[i + 1]
            for x in range(x0, x1):
                pixels_filled.append((x, y))
    
    def increment_x(AET: dict):
        for _, edge_val in AET.items():
            edge_val['x'] += edge_val['inv_m']

    n = len(P)
    if n < 3:
        return []

    pixels_filled = []
    ind = sorted(range(n), key=lambda index: P[index].y())
    y_min = math.ceil(P[ind[0]].y())
    y_max = math.ceil(P[ind[n - 1]].y()) - 1
    AET = {}
    i = 0
    y = y_min
    while y <= y_max:
        # Process all vertices lying on current scanline
        while y == math.ceil(P[ind[i]].y()) and i < n:
            curr_idx = ind[i]
            prev_idx = (ind[i] - 1) % n
            next_idx = (ind[i] + 1) % n
            update_AET(curr_idx, prev_idx, next_idx, P, AET)
            i += 1
        x_values = [math.ceil(edge_val['x']) for (_, edge_val) in AET.items()]
        x_values.sort()
        fill(x_values, y, pixels_filled)
        increment_x(AET)
        y += 1

    return pixels_filled
