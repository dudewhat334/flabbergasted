from PyQt5 import QtWidgets, QtGui, QtCore
from config import BACKGROUND_PATH

class ToolsWindow(QtWidgets.QWidget):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.setWindowTitle("Tools")
        self.setFixedSize(380, 320)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(0, 0)
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

        title_font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        title_font.setItalic(True)
        self.title = QtWidgets.QLabel("TOOLS", self)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)

        # --- Bunny Hop Interval Slider ---
        self.bhop_interval_label = QtWidgets.QLabel(
            f"Bunny Hop Interval (ms): {self.state.get('bunnyhop_interval', 40)}", self
        )
        self.bhop_interval_label.setStyleSheet("color: white;")
        layout.addWidget(self.bhop_interval_label)

        self.bhop_interval_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.bhop_interval_slider.setMinimum(10)
        self.bhop_interval_slider.setMaximum(300)
        self.bhop_interval_slider.setValue(self.state.get('bunnyhop_interval', 40))
        self.bhop_interval_slider.valueChanged.connect(self.set_bhop_interval)
        layout.addWidget(self.bhop_interval_slider)

        # --- Bunny Hop Checkbox ---
        self.bunnyhop_checkbox = QtWidgets.QCheckBox("Enable Bunny Hop", self)
        self.bunnyhop_checkbox.setStyleSheet("color: white;")
        self.bunnyhop_checkbox.setChecked(self.state.get('bunnyhop_enabled', False))
        self.bunnyhop_checkbox.stateChanged.connect(self.toggle_bunnyhop)
        layout.addWidget(self.bunnyhop_checkbox)

        layout.addStretch(1)  # Pushes the Back button to the bottom

        self.back_btn = QtWidgets.QPushButton("Back")
        self.back_btn.setFont(title_font)
        self.back_btn.setStyleSheet("color: green; background-color: black; border: 1px solid green;")
        self.back_btn.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def back_to_main(self):
        self.main_window.move(self.pos())
        self.main_window.show()
        self.hide()

    def set_menu_opacity(self, opacity):
        opacity = float(opacity)
        self.setWindowOpacity(opacity)

    def set_bhop_interval(self, value):
        self.state['bunnyhop_interval'] = value
        self.bhop_interval_label.setText(f"Bunny Hop Interval (ms): {value}")

    def toggle_bunnyhop(self, state):
        enabled = state == QtCore.Qt.Checked
        self.state['bunnyhop_enabled'] = enabled