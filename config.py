from PySide6.QtGui import QColor

SCALE = 50 # Parameter for scaling the size of bezier surface on the canvas
LIGHT_SOURCE_RADIUS = 3 * SCALE
LIGHT_SOURCE_SPEED = 0.5 # Radians per second
DEFAULT_LIGHT_COLOR = QColor(255, 255, 255) # White
DEFAULT_SURFACE_COLOR = QColor(0, 255, 255) # Cyan
ANIMATION_FPS = 60