from PySide6.QtCore import QTimer, QElapsedTimer

import config

class Animation:
    def __init__(self, func, fps=config.ANIMATION_FPS):
        self.interval_ms = int(1000 / max(1, fps))
        self.tick_timer = QTimer()
        self.tick_timer.timeout.connect(func)
        self.elapsed_timer = QElapsedTimer()
        self.paused = False
        self.pause_start_time = None
        self.total_paused_time = 0
    
    def run(self):
        self.tick_timer.start(self.interval_ms)
        self.elapsed_timer.start()

    def resume(self):
        if self.paused:
            if self.pause_start_time is not None:
                self.total_paused_time += self.elapsed_timer.elapsed() - self.pause_start_time
                self.pause_start_time = None
            self.tick_timer.start(self.interval_ms)
            self.paused = False

    def pause(self):
        if not self.paused:
            self.tick_timer.stop()
            self.pause_start_time = self.elapsed_timer.elapsed()
            self.paused = True

    def get_active_time(self):
        return self.elapsed_timer.elapsed() - self.total_paused_time