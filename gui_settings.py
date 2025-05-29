from PyQt5 import QtWidgets, QtCore, QtGui
from config import BACKGROUND_PATH

class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.setFixedSize(380, 320)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(0, 0)

        # Set up the background image
        self.background = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(BACKGROUND_PATH)
        if pixmap.isNull():
            print(f"Error loading background image at: {BACKGROUND_PATH}")
        self.background.setPixmap(
            pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        )
        self.background.setGeometry(0, 0, 380, 320)
        self.background.lower()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(10)

        # Title styling
        title_font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        title_font.setItalic(True)
        self.title = QtWidgets.QLabel("SETTINGS", self)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)

        # Always On Checkbox
        self.always_on_checkbox = QtWidgets.QCheckBox("Always On")
        self.always_on_checkbox.setChecked(self.state.get("crosshair_always_on", True))
        self.always_on_checkbox.setStyleSheet("color: white; font-size: 12pt;")
        self.always_on_checkbox.stateChanged.connect(self.on_always_on_changed)
        layout.addWidget(self.always_on_checkbox)

        # Hide Overlay Checkbox
        self.hide_overlay_checkbox = QtWidgets.QCheckBox("Hide Overlay")
        self.hide_overlay_checkbox.setChecked(self.state.get("hide_overlay", False))
        self.hide_overlay_checkbox.setStyleSheet("color: white; font-size: 12pt;")
        self.hide_overlay_checkbox.stateChanged.connect(self.on_hide_overlay_changed)
        layout.addWidget(self.hide_overlay_checkbox)

        # Example: add more settings widgets here if you have other features
        # Example:
        # self.some_other_checkbox = QtWidgets.QCheckBox("Some Other Feature")
        # layout.addWidget(self.some_other_checkbox)

        layout.addStretch(1)

        # Back button styling
        self.back_btn = QtWidgets.QPushButton("Back")
        self.back_btn.setFont(title_font)
        self.back_btn.setStyleSheet("color: green; background-color: black; border: 1px solid green;")
        self.back_btn.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def on_always_on_changed(self, state):
        self.state["crosshair_always_on"] = (state == QtCore.Qt.Checked)
        self.main_window.overlay_window.update_crosshair_visibility()

    def on_hide_overlay_changed(self, state):
        self.state["hide_overlay"] = (state == QtCore.Qt.Checked)
        self.main_window.overlay_window.update_crosshair_visibility()

    def set_menu_opacity(self, opacity):
        self.setWindowOpacity(float(opacity))

    def back_to_main(self):
        self.main_window.move(self.pos())
        self.main_window.show()
        self.hide()