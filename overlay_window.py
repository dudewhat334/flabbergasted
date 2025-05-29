from PyQt5 import QtCore, QtGui, QtWidgets
from pynput import mouse

# You'll want to import PRESETS from your config or similar location
from config import PRESETS

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        geometry = QtWidgets.QApplication.desktop().screenGeometry()
        self.setGeometry(geometry)

        self.rmb_down = False
        self.crosshair_should_be_drawn = False

        # Listen for mouse button events in background
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

        # Always show the overlay, just change opacity
        self.show()
        # Initial update to set opacity
        QtCore.QTimer.singleShot(0, self.update_crosshair_visibility)

    def on_click(self, x, y, button, pressed):
        from pynput.mouse import Button
        if button == Button.right:
            self.rmb_down = pressed
            print(f"[DEBUG] RMB {'pressed' if pressed else 'released'}")
            QtCore.QMetaObject.invokeMethod(
                self, "update_crosshair_visibility", QtCore.Qt.QueuedConnection
            )

    @QtCore.pyqtSlot()
    def update_crosshair_visibility(self):
        print("[DEBUG] update_crosshair_visibility called")
        if self.state.get("hide_overlay", False):
            print("[DEBUG] hide_overlay is True, setting opacity to 0")
            self.crosshair_should_be_drawn = False
            self.setWindowOpacity(0.0)
            self.update()
            return

        selected_preset = self.state.get("selected_preset")
        if selected_preset not in PRESETS:
            print(f"[DEBUG] selected_preset '{selected_preset}' is not in PRESETS list! Setting opacity to 0.")
            self.crosshair_should_be_drawn = False
            self.setWindowOpacity(0.0)
            self.update()
            return

        redicals = self.state.get("redicals", {})
        preset_settings = redicals.get(selected_preset, {})

        print(f"[DEBUG] selected_preset: {selected_preset}")
        print(f"[DEBUG] preset_settings: {preset_settings}")
        print(f"[DEBUG] rmb_down: {self.rmb_down}")

        # Only allow drawing if always_on or toggle_mode+RMB is active
        if preset_settings.get("always_on", False):
            print("[DEBUG] always_on is True for selected preset")
            self.crosshair_should_be_drawn = True
        elif preset_settings.get("toggle_mode", False) and self.rmb_down:
            print("[DEBUG] toggle_mode is True and RMB is down for selected preset")
            self.crosshair_should_be_drawn = True
        else:
            print("[DEBUG] Crosshair should NOT be drawn")
            self.crosshair_should_be_drawn = False

        if self.crosshair_should_be_drawn:
            print("[DEBUG] Setting opacity to 1.0 (visible)")
            self.setWindowOpacity(1.0)
        else:
            print("[DEBUG] Setting opacity to 0.0 (invisible)")
            self.setWindowOpacity(0.0)
        self.update()

    def paintEvent(self, event):
        if not self.crosshair_should_be_drawn:
            print("[DEBUG] paintEvent: crosshair_should_be_drawn is False, nothing to draw")
            return

        painter = QtGui.QPainter(self)
        center = self.rect().center()
        preset = self.state.get("selected_preset")
        print(f"[DEBUG] paintEvent drawing for preset: {preset}")

        pen = QtGui.QPen(QtCore.Qt.green, 3)
        if preset == "rifle":
            pen.setColor(QtCore.Qt.red)
        elif preset == "dot":
            pen.setColor(QtCore.Qt.yellow)
        elif preset == "cross":
            pen.setColor(QtCore.Qt.green)
        elif preset == "circle":
            pen.setColor(QtCore.Qt.cyan)
        elif preset == "chevron":
            pen.setColor(QtCore.Qt.magenta)
        painter.setPen(pen)

        if preset == "cross":
            painter.drawLine(center.x() - 20, center.y(), center.x() + 20, center.y())
            painter.drawLine(center.x(), center.y() - 20, center.x(), center.y() + 20)
        elif preset == "dot":
            painter.setBrush(QtGui.QBrush(pen.color()))
            painter.drawEllipse(center, 6, 6)
        elif preset == "rifle":
            painter.drawEllipse(center, 30, 30)
            painter.drawLine(center.x() - 40, center.y(), center.x() + 40, center.y())
            painter.drawLine(center.x(), center.y() - 40, center.x(), center.y() + 40)
        elif preset == "circle":
            painter.drawEllipse(center, 29, 29)
        elif preset == "chevron":
            path = QtGui.QPainterPath()
            path.moveTo(center.x() - 15, center.y() - 10)
            path.lineTo(center.x(), center.y() + 15)
            path.lineTo(center.x() + 15, center.y() - 10)
            painter.drawPath(path)

        painter.end()