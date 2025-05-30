from PyQt5 import QtWidgets, QtCore, QtGui
from config import save_config, BACKGROUND_PATH

class ToolsWindow(QtWidgets.QWidget):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.setWindowTitle("Tools")
        self.setFixedSize(380, 420)
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
        self.background.setGeometry(0, 0, 380, 420)
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

        # --- AFK Prevent Controls ---
        self.afk_checkbox = QtWidgets.QCheckBox("Enable AFK Kick Prevention", self)
        self.afk_checkbox.setStyleSheet("color: white;")
        self.afk_checkbox.setChecked(self.state.get('afk_enabled', False))
        self.afk_checkbox.stateChanged.connect(self.toggle_afk)
        layout.addWidget(self.afk_checkbox)

        self.afk_amount_label = QtWidgets.QLabel(
            f"AFK Move Amount (s): {self.state.get('afk_move_amount', 0.01):.3f}", self
        )
        self.afk_amount_label.setStyleSheet("color: white;")
        layout.addWidget(self.afk_amount_label)

        # Slider: 10 (0.01s) to 1000 (1.0s), for extra smooth fine control
        self.afk_amount_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.afk_amount_slider.setMinimum(10)    # 0.01s minimum (games won't register lower)
        self.afk_amount_slider.setMaximum(1000)  # 1.0s max (very large step)
        default_amount = int(self.state.get('afk_move_amount', 0.01) * 1000)
        self.afk_amount_slider.setValue(default_amount)
        self.afk_amount_slider.setSingleStep(1)
        self.afk_amount_slider.setPageStep(10)
        self.afk_amount_slider.valueChanged.connect(self.set_afk_amount)
        layout.addWidget(self.afk_amount_slider)

        self.afk_interval_label = QtWidgets.QLabel(
            f"AFK Move Interval (s): {self.state.get('afk_move_interval', 1.0):.2f}", self
        )
        self.afk_interval_label.setStyleSheet("color: white;")
        layout.addWidget(self.afk_interval_label)

        self.afk_interval_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.afk_interval_slider.setMinimum(1)
        self.afk_interval_slider.setMaximum(10)
        self.afk_interval_slider.setValue(int(self.state.get('afk_move_interval', 1.0)))
        self.afk_interval_slider.valueChanged.connect(self.set_afk_interval)
        layout.addWidget(self.afk_interval_slider)

        self.afk_return_checkbox = QtWidgets.QCheckBox("Return to Home After AFK", self)
        self.afk_return_checkbox.setStyleSheet("color: white;")
        self.afk_return_checkbox.setChecked(self.state.get('afk_return_home', False))
        self.afk_return_checkbox.stateChanged.connect(self.toggle_afk_return_home)
        layout.addWidget(self.afk_return_checkbox)

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

    def set_bhop_interval(self, value):
        self.state['bunnyhop_interval'] = value
        self.bhop_interval_label.setText(f"Bunny Hop Interval (ms): {value}")
        save_config(self.state)

    def toggle_bunnyhop(self, state):
        enabled = state == QtCore.Qt.Checked
        self.state['bunnyhop_enabled'] = enabled
        save_config(self.state)

    def set_afk_amount(self, value):
        duration = value / 1000.0  # 10-1000 -> 0.01 - 1.0 seconds
        self.state['afk_move_amount'] = duration
        self.afk_amount_label.setText(f"AFK Move Amount (s): {duration:.3f}")
        save_config(self.state)

    def set_afk_interval(self, value):
        interval = float(value)
        self.state['afk_move_interval'] = interval
        self.afk_interval_label.setText(f"AFK Move Interval (s): {interval:.2f}")
        save_config(self.state)

    def toggle_afk(self, state):
        enabled = state == QtCore.Qt.Checked
        self.state['afk_enabled'] = enabled
        save_config(self.state)

    def toggle_afk_return_home(self, state):
        enabled = state == QtCore.Qt.Checked
        self.state['afk_return_home'] = enabled
        save_config(self.state)

    def set_menu_opacity(self, opacity):
        self.setWindowOpacity(float(opacity))

    def set_bhop_macro_key(self, value):
        self.state['bunnyhop_macro_key'] = value
        save_config(self.state)