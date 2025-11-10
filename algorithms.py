from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter

def scanline_filling(P: list[QPointF], painter: QPainter):
    def update_AET(P_current: QPointF, P_prev: QPointF, P_next: QPointF, AET: dict):
        # Updating previous edge
        prev_edge = eval_AET_edge(P_prev, P_current, y)
        if prev_edge is not None:
            if P_prev.y() >= P_current.y():
                AET[(P_prev, P_current)] = prev_edge
            else:
                del AET[(P_prev, P_current)]
        # Updating next edge
        next_edge = eval_AET_edge(P_current, P_next, y)
        if next_edge is not None:
            if P_next.y() >= P_current.y():
                AET[(P_current, P_next)] = next_edge
            else:
                del AET[(P_current, P_next)]
        
    def eval_AET_edge(p0: QPointF, p1: QPointF, scan_line: float):
        # Ignore horizontal edges
        if p0.y() == p1.y():
            return None
        
        # Ensure p_lower has smaller y (or equal y but smaller x)
        if (p0.y(), p0.x()) < (p1.y(), p1.x()):
            p_lower, p_upper = p0, p1
        else:
            p_lower, p_upper = p1, p0

        dx = p_upper.x() - p_lower.x()
        dy = p_upper.y() - p_lower.y()
        inv_m = dx / dy # 1 / m
        x_intersection = p_lower.x() + (scan_line - p_lower.y()) * inv_m

        return {
            'x': x_intersection,
            'inv_m': inv_m
        }

    def fill(x_values: list[int], y: int, painter: QPainter):
        for i in range(0, len(x_values), 2):
            x0 = x_values[i]
            x1 = x_values[i + 1]
            painter.drawLine(x0, y, x1, y)
    
    def increment_x(AET: dict):
        for _, edge_val in AET.items():
            edge_val['x'] += edge_val['inv_m']

    n = len(P)
    if n < 3:
        return

    ind = sorted(range(n), key=lambda index: P[index].y())
    y_min = int(round(P[ind[0]].y()))
    y_max = int(round(P[ind[n - 1]].y()))
    AET = {}
    i = 0
    y = y_min
    while y <= y_max:
        while i < n and y == int(round(P[ind[i]].y())): # Przetwarzamy wszystkie wierzchołki leżące na biężącej linii y
            P_current = P[ind[i]]
            P_prev = P[(ind[i] - 1) % n]
            P_next = P[(ind[i] + 1) % n]
            update_AET(P_current, P_prev, P_next, AET)
            i += 1
        x_values = [int(round(edge_val['x'])) for (_, edge_val) in AET.items()]
        x_values.sort()
        fill(x_values, y, painter)
        increment_x(AET)
        y += 1

