from PyQt5 import QtWidgets, QtGui, QtCore
from config import PRESETS, BACKGROUND_PATH, save_config
from color_button import ColorButton

class RedicalSettingsWindow(QtWidgets.QWidget):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.setWindowTitle("Redical Settings")
        self.setFixedSize(400, 700)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # --- Background Label (created FIRST) ---
        self.background = QtWidgets.QLabel(self)
        self.background.setObjectName("background_label")
        self._set_background_pixmap()

        # --- SCROLL AREA ---
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("""
QScrollArea {
    background: transparent;
}
QScrollBar:vertical {
    background: #181818;
    border: 1px solid #111;
    width: 20px;
    margin: 0;
    border-radius: 10px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #33ff33, stop:1 #009900
    );
    min-height: 24px;
    max-height: 40px;
    border-radius: 8px;
    border: 2px solid #222;
    margin: 2px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
    border: none;
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    width: 0px;
    height: 0px;
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
""")

        # --- Content Widget for Scroll Area ---
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(10)

        # --- Title ---
        title_font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        title_font.setItalic(True)
        self.title = QtWidgets.QLabel("REDICAL SETTINGS", self)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)

        # --- Recenter Button ---
        self.recenter_btn = QtWidgets.QPushButton("Recenter This Reticle")
        self.recenter_btn.setStyleSheet("color: orange; background-color: #222; border: 1px solid orange;")
        self.recenter_btn.clicked.connect(self.recenter_current_reticle)
        layout.addWidget(self.recenter_btn)

        # --- Preset Selector ---
        self.preset_box = QtWidgets.QComboBox()
        self.preset_keys = list(PRESETS.keys())
        self.preset_box.addItems(PRESETS.values())
        current_idx = self.preset_keys.index(self.state.get("selected_preset", self.preset_keys[0]))
        self.preset_box.setCurrentIndex(current_idx)
        self.preset_box.currentIndexChanged.connect(self.change_preset)
        self.preset_box.setStyleSheet("""
            QComboBox { color: white; background-color: #222; }
            QComboBox QAbstractItemView { color: black; background: white; }
        """)
        layout.addWidget(self.preset_box)

        # --- Per-preset visibility controls ---
        self.always_on_checkbox = QtWidgets.QCheckBox("Always On")
        self.always_on_checkbox.setStyleSheet("color: white; font-size: 12pt;")
        self.always_on_checkbox.stateChanged.connect(self.on_always_on_changed)
        layout.addWidget(self.always_on_checkbox)
        self.toggle_mode_checkbox = QtWidgets.QCheckBox("Toggle Mode (RMB)")
        self.toggle_mode_checkbox.setStyleSheet("color: white; font-size: 12pt;")
        self.toggle_mode_checkbox.stateChanged.connect(self.on_toggle_mode_changed)
        layout.addWidget(self.toggle_mode_checkbox)

        # --- Reticle Scaling ---
        overall_layout = QtWidgets.QFormLayout()
        self.overall_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.overall_size_slider.setMinimum(5)
        self.overall_size_slider.setMaximum(300)
        self.overall_width_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.overall_width_slider.setMinimum(5)
        self.overall_width_slider.setMaximum(300)
        self.overall_size_slider.valueChanged.connect(self.set_overall_size)
        self.overall_width_slider.valueChanged.connect(self.set_overall_width)
        overall_layout.addRow(self.make_white_label("Overall Size:"), self.overall_size_slider)
        overall_layout.addRow(self.make_white_label("Overall Width:"), self.overall_width_slider)
        overall_box = QtWidgets.QGroupBox("Reticle Scaling")
        overall_box.setLayout(overall_layout)
        layout.addWidget(overall_box)

        # --- Rifle Controls ---
        self.rifle_controls = QtWidgets.QGroupBox("Rifle Scope Controls")
        rifle_layout = QtWidgets.QFormLayout()
        self.rifle_circle_color_btn = ColorButton(self.state["rifle_circle_color"], self.set_rifle_circle_color)
        rifle_layout.addRow(self.make_white_label("Circle Color:"), self.rifle_circle_color_btn)
        self.rifle_circle_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle_circle_radius_slider.setMinimum(20)
        self.rifle_circle_radius_slider.setMaximum(500)
        self.rifle_circle_radius_slider.setValue(self.state["rifle_circle_radius"])
        self.rifle_circle_radius_slider.valueChanged.connect(self.set_rifle_circle_radius)
        rifle_layout.addRow(self.make_white_label("Circle Radius:"), self.rifle_circle_radius_slider)
        self.rifle_circle_width_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle_circle_width_slider.setMinimum(1)
        self.rifle_circle_width_slider.setMaximum(20)
        self.rifle_circle_width_slider.setValue(self.state["rifle_circle_width"])
        self.rifle_circle_width_slider.valueChanged.connect(self.set_rifle_circle_width)
        rifle_layout.addRow(self.make_white_label("Circle Width:"), self.rifle_circle_width_slider)
        self.rifle_cross_color_btn = ColorButton(self.state["rifle_cross_color"], self.set_rifle_cross_color)
        rifle_layout.addRow(self.make_white_label("Cross Color:"), self.rifle_cross_color_btn)
        self.rifle_cross_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle_cross_length_slider.setMinimum(10)
        self.rifle_cross_length_slider.setMaximum(400)
        self.rifle_cross_length_slider.setValue(self.state["rifle_cross_length"])
        self.rifle_cross_length_slider.valueChanged.connect(self.set_rifle_cross_length)
        rifle_layout.addRow(self.make_white_label("Cross Length:"), self.rifle_cross_length_slider)
        self.rifle_cross_thickness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle_cross_thickness_slider.setMinimum(1)
        self.rifle_cross_thickness_slider.setMaximum(16)
        self.rifle_cross_thickness_slider.setValue(self.state["rifle_cross_thickness"])
        self.rifle_cross_thickness_slider.valueChanged.connect(self.set_rifle_cross_thickness)
        rifle_layout.addRow(self.make_white_label("Cross Thickness:"), self.rifle_cross_thickness_slider)
        self.rifle_center_dot_color_btn = ColorButton(self.state["rifle_center_dot_color"], self.set_rifle_center_dot_color)
        rifle_layout.addRow(self.make_white_label("Center Dot Color:"), self.rifle_center_dot_color_btn)
        self.rifle_center_dot_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle_center_dot_radius_slider.setMinimum(1)
        self.rifle_center_dot_radius_slider.setMaximum(30)
        self.rifle_center_dot_radius_slider.setValue(self.state["rifle_center_dot_radius"])
        self.rifle_center_dot_radius_slider.valueChanged.connect(self.set_rifle_center_dot_radius)
        rifle_layout.addRow(self.make_white_label("Center Dot Radius:"), self.rifle_center_dot_radius_slider)
        self.rifle_controls.setLayout(rifle_layout)
        layout.addWidget(self.rifle_controls)

        # --- Rifle2 Controls ---
        self.rifle2_controls = QtWidgets.QGroupBox("Rifle Scope (Elevation/Wind) Controls")
        rifle2_layout = QtWidgets.QFormLayout()
        self.rifle2_circle_color_btn = ColorButton(self.state["rifle2_circle_color"], self.set_rifle2_circle_color)
        rifle2_layout.addRow(self.make_white_label("Circle Color:"), self.rifle2_circle_color_btn)
        self.rifle2_circle_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_circle_radius_slider.setMinimum(20)
        self.rifle2_circle_radius_slider.setMaximum(500)
        self.rifle2_circle_radius_slider.setValue(self.state["rifle2_circle_radius"])
        self.rifle2_circle_radius_slider.valueChanged.connect(self.set_rifle2_circle_radius)
        rifle2_layout.addRow(self.make_white_label("Circle Radius:"), self.rifle2_circle_radius_slider)
        self.rifle2_circle_width_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_circle_width_slider.setMinimum(1)
        self.rifle2_circle_width_slider.setMaximum(20)
        self.rifle2_circle_width_slider.setValue(self.state["rifle2_circle_width"])
        self.rifle2_circle_width_slider.valueChanged.connect(self.set_rifle2_circle_width)
        rifle2_layout.addRow(self.make_white_label("Circle Width:"), self.rifle2_circle_width_slider)
        self.rifle2_cross_color_btn = ColorButton(self.state["rifle2_cross_color"], self.set_rifle2_cross_color)
        rifle2_layout.addRow(self.make_white_label("Cross Color:"), self.rifle2_cross_color_btn)
        self.rifle2_cross_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_cross_length_slider.setMinimum(10)
        self.rifle2_cross_length_slider.setMaximum(400)
        self.rifle2_cross_length_slider.setValue(self.state["rifle2_cross_length"])
        self.rifle2_cross_length_slider.valueChanged.connect(self.set_rifle2_cross_length)
        rifle2_layout.addRow(self.make_white_label("Cross Length:"), self.rifle2_cross_length_slider)
        self.rifle2_cross_thickness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_cross_thickness_slider.setMinimum(1)
        self.rifle2_cross_thickness_slider.setMaximum(16)
        self.rifle2_cross_thickness_slider.setValue(self.state["rifle2_cross_thickness"])
        self.rifle2_cross_thickness_slider.valueChanged.connect(self.set_rifle2_cross_thickness)
        rifle2_layout.addRow(self.make_white_label("Cross Thickness:"), self.rifle2_cross_thickness_slider)
        self.rifle2_center_dot_color_btn = ColorButton(self.state["rifle2_center_dot_color"], self.set_rifle2_center_dot_color)
        rifle2_layout.addRow(self.make_white_label("Center Dot Color:"), self.rifle2_center_dot_color_btn)
        self.rifle2_center_dot_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_center_dot_radius_slider.setMinimum(1)
        self.rifle2_center_dot_radius_slider.setMaximum(30)
        self.rifle2_center_dot_radius_slider.setValue(self.state["rifle2_center_dot_radius"])
        self.rifle2_center_dot_radius_slider.valueChanged.connect(self.set_rifle2_center_dot_radius)
        rifle2_layout.addRow(self.make_white_label("Center Dot Radius:"), self.rifle2_center_dot_radius_slider)
        self.rifle2_elevation_lines_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_elevation_lines_slider.setMinimum(0)
        self.rifle2_elevation_lines_slider.setMaximum(8)
        self.rifle2_elevation_lines_slider.setValue(self.state.get("rifle2_elevation_lines", 3))
        self.rifle2_elevation_lines_slider.valueChanged.connect(self.set_rifle2_elevation_lines)
        rifle2_layout.addRow(self.make_white_label("Elevation Lines:"), self.rifle2_elevation_lines_slider)
        self.rifle2_elevation_spacing_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_elevation_spacing_slider.setMinimum(10)
        self.rifle2_elevation_spacing_slider.setMaximum(100)
        self.rifle2_elevation_spacing_slider.setValue(self.state.get("rifle2_elevation_spacing", 25))
        self.rifle2_elevation_spacing_slider.valueChanged.connect(self.set_rifle2_elevation_spacing)
        rifle2_layout.addRow(self.make_white_label("Elevation Spacing:"), self.rifle2_elevation_spacing_slider)
        self.rifle2_elevation_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_elevation_length_slider.setMinimum(10)
        self.rifle2_elevation_length_slider.setMaximum(400)
        self.rifle2_elevation_length_slider.setValue(self.state.get("rifle2_elevation_length", 60))
        self.rifle2_elevation_length_slider.valueChanged.connect(self.set_rifle2_elevation_length)
        rifle2_layout.addRow(self.make_white_label("Elevation Bar Length:"), self.rifle2_elevation_length_slider)
        self.rifle2_wind_lines_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_wind_lines_slider.setMinimum(0)
        self.rifle2_wind_lines_slider.setMaximum(8)
        self.rifle2_wind_lines_slider.setValue(self.state.get("rifle2_wind_lines", 2))
        self.rifle2_wind_lines_slider.valueChanged.connect(self.set_rifle2_wind_lines)
        rifle2_layout.addRow(self.make_white_label("Wind Lines:"), self.rifle2_wind_lines_slider)
        self.rifle2_wind_spacing_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_wind_spacing_slider.setMinimum(10)
        self.rifle2_wind_spacing_slider.setMaximum(100)
        self.rifle2_wind_spacing_slider.setValue(self.state.get("rifle2_wind_spacing", 25))
        self.rifle2_wind_spacing_slider.valueChanged.connect(self.set_rifle2_wind_spacing)
        rifle2_layout.addRow(self.make_white_label("Wind Line Spacing:"), self.rifle2_wind_spacing_slider)
        self.rifle2_wind_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_wind_length_slider.setMinimum(10)
        self.rifle2_wind_length_slider.setMaximum(200)
        self.rifle2_wind_length_slider.setValue(self.state.get("rifle2_wind_length", 40))
        self.rifle2_wind_length_slider.valueChanged.connect(self.set_rifle2_wind_length)
        rifle2_layout.addRow(self.make_white_label("Wind Line Length:"), self.rifle2_wind_length_slider)
        self.rifle2_wind_height_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rifle2_wind_height_slider.setMinimum(-100)
        self.rifle2_wind_height_slider.setMaximum(100)
        self.rifle2_wind_height_slider.setValue(self.state.get("rifle2_wind_height", 25))
        self.rifle2_wind_height_slider.valueChanged.connect(self.set_rifle2_wind_height)
        rifle2_layout.addRow(self.make_white_label("Wind Line Height Offset:"), self.rifle2_wind_height_slider)
        self.rifle2_wind_side_box = QtWidgets.QComboBox()
        self.rifle2_wind_side_box.addItems(["left", "right", "both"])
        self.rifle2_wind_side_box.setCurrentText(self.state.get("rifle2_wind_side", "left"))
        self.rifle2_wind_side_box.setStyleSheet("""
            QComboBox { color: white; background-color: #222; }
            QComboBox QAbstractItemView { color: black; background: white; }
        """)
        self.rifle2_wind_side_box.currentTextChanged.connect(self.set_rifle2_wind_side)
        rifle2_layout.addRow(self.make_white_label("Wind Line Side:"), self.rifle2_wind_side_box)
        self.rifle2_controls.setLayout(rifle2_layout)
        layout.addWidget(self.rifle2_controls)

        # --- Dot Controls ---
        self.dot_controls = QtWidgets.QGroupBox("Dot Controls")
        dot_layout = QtWidgets.QFormLayout()
        self.dot_color_btn = ColorButton(self.state["dot_color"], self.set_dot_color)
        dot_layout.addRow(self.make_white_label("Dot Color:"), self.dot_color_btn)
        self.dot_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.dot_radius_slider.setMinimum(1)
        self.dot_radius_slider.setMaximum(60)
        self.dot_radius_slider.setValue(self.state["dot_radius"])
        self.dot_radius_slider.valueChanged.connect(self.set_dot_radius)
        dot_layout.addRow(self.make_white_label("Dot Radius:"), self.dot_radius_slider)
        self.dot_controls.setLayout(dot_layout)
        layout.addWidget(self.dot_controls)

        # --- Cross Controls ---
        self.cross_controls = QtWidgets.QGroupBox("Cross Controls")
        cross_layout = QtWidgets.QFormLayout()
        self.cross_color_btn = ColorButton(self.state["cross_color"], self.set_cross_color)
        cross_layout.addRow(self.make_white_label("Cross Color:"), self.cross_color_btn)
        self.cross_length_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.cross_length_slider.setMinimum(5)
        self.cross_length_slider.setMaximum(200)
        self.cross_length_slider.setValue(self.state["cross_length"])
        self.cross_length_slider.valueChanged.connect(self.set_cross_length)
        cross_layout.addRow(self.make_white_label("Cross Length:"), self.cross_length_slider)
        self.cross_thickness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.cross_thickness_slider.setMinimum(1)
        self.cross_thickness_slider.setMaximum(12)
        self.cross_thickness_slider.setValue(self.state["cross_thickness"])
        self.cross_thickness_slider.valueChanged.connect(self.set_cross_thickness)
        cross_layout.addRow(self.make_white_label("Cross Thickness:"), self.cross_thickness_slider)
        self.cross_controls.setLayout(cross_layout)
        layout.addWidget(self.cross_controls)

        # --- Circle Controls ---
        self.circle_controls = QtWidgets.QGroupBox("Circle Controls")
        circle_layout = QtWidgets.QFormLayout()
        self.circle_color_btn = ColorButton(self.state["circle_color"], self.set_circle_color)
        circle_layout.addRow(self.make_white_label("Circle Color:"), self.circle_color_btn)
        self.circle_radius_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.circle_radius_slider.setMinimum(5)
        self.circle_radius_slider.setMaximum(200)
        self.circle_radius_slider.setValue(self.state["circle_radius"])
        self.circle_radius_slider.valueChanged.connect(self.set_circle_radius)
        circle_layout.addRow(self.make_white_label("Circle Radius:"), self.circle_radius_slider)
        self.circle_width_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.circle_width_slider.setMinimum(1)
        self.circle_width_slider.setMaximum(16)
        self.circle_width_slider.setValue(self.state["circle_width"])
        self.circle_width_slider.valueChanged.connect(self.set_circle_width)
        circle_layout.addRow(self.make_white_label("Circle Width:"), self.circle_width_slider)
        self.circle_controls.setLayout(circle_layout)
        layout.addWidget(self.circle_controls)

        # --- Chevron Controls ---
        self.chevron_controls = QtWidgets.QGroupBox("Chevron Controls")
        chevron_layout = QtWidgets.QFormLayout()
        self.chevron_color_btn = ColorButton(self.state["chevron_color"], self.set_chevron_color)
        chevron_layout.addRow(self.make_white_label("Chevron Color:"), self.chevron_color_btn)
        self.chevron_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.chevron_size_slider.setMinimum(5)
        self.chevron_size_slider.setMaximum(100)
        self.chevron_size_slider.setValue(self.state["chevron_size"])
        self.chevron_size_slider.valueChanged.connect(self.set_chevron_size)
        chevron_layout.addRow(self.make_white_label("Chevron Size:"), self.chevron_size_slider)
        self.chevron_thickness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.chevron_thickness_slider.setMinimum(1)
        self.chevron_thickness_slider.setMaximum(12)
        self.chevron_thickness_slider.setValue(self.state["chevron_thickness"])
        self.chevron_thickness_slider.valueChanged.connect(self.set_chevron_thickness)
        chevron_layout.addRow(self.make_white_label("Chevron Thickness:"), self.chevron_thickness_slider)
        self.chevron_controls.setLayout(chevron_layout)
        layout.addWidget(self.chevron_controls)

        # --- Back Button ---
        self.back_btn = QtWidgets.QPushButton("Back")
        self.back_btn.setFont(title_font)
        self.back_btn.setStyleSheet("color: green; background-color: black; border: 1px solid green;")
        self.back_btn.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_btn)

        scroll_area.setWidget(content_widget)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # --- Make sure the background is always at the back ---
        self.background.lower()

        self.update_controls()

    def _set_background_pixmap(self):
        pixmap = QtGui.QPixmap(BACKGROUND_PATH)
        if pixmap.isNull():
            print(f"Error loading background image at: {BACKGROUND_PATH}")
            self.background.setStyleSheet("background: #222; border-radius: 12px;")
            self.background.setPixmap(QtGui.QPixmap())  # Clear previous pixmap
        else:
            self.background.setStyleSheet("")  # Clear fallback style
            self.background.setPixmap(
                pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            )
        self.background.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self._set_background_pixmap()
        super().resizeEvent(event)

    def make_white_label(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("color: white;")
        return label

    def change_preset(self, idx):
        key = self.preset_keys[idx]
        self.state["selected_preset"] = key
        save_config(self.state)
        self.update_controls()

    def update_controls(self):
        preset = self.state["selected_preset"]
        size = int(self.state.get(f"{preset}_overall_size", 1.0) * 100)
        width = int(self.state.get(f"{preset}_overall_width", 1.0) * 100)
        self.overall_size_slider.blockSignals(True)
        self.overall_width_slider.blockSignals(True)
        self.overall_size_slider.setValue(size)
        self.overall_width_slider.setValue(width)
        self.overall_size_slider.blockSignals(False)
        self.overall_width_slider.blockSignals(False)
        self.rifle_controls.setVisible(preset == "rifle")
        self.rifle2_controls.setVisible(preset == "rifle2")
        self.dot_controls.setVisible(preset == "dot")
        self.cross_controls.setVisible(preset == "cross")
        self.circle_controls.setVisible(preset == "circle")
        self.chevron_controls.setVisible(preset == "chevron")
        preset_state = self.state.get("redicals", {}).get(preset, {})
        self.always_on_checkbox.blockSignals(True)
        self.toggle_mode_checkbox.blockSignals(True)
        self.always_on_checkbox.setChecked(preset_state.get("always_on", False))
        self.toggle_mode_checkbox.setChecked(preset_state.get("toggle_mode", False))
        self.always_on_checkbox.blockSignals(False)
        self.toggle_mode_checkbox.blockSignals(False)

    def on_always_on_changed(self, val):
        preset = self.state["selected_preset"]
        if "redicals" not in self.state:
            self.state["redicals"] = {}
        if preset not in self.state["redicals"]:
            self.state["redicals"][preset] = {}
        self.state["redicals"][preset]["always_on"] = (val == QtCore.Qt.Checked)
        save_config(self.state)

    def on_toggle_mode_changed(self, val):
        preset = self.state["selected_preset"]
        if "redicals" not in self.state:
            self.state["redicals"] = {}
        if preset not in self.state["redicals"]:
            self.state["redicals"][preset] = {}
        self.state["redicals"][preset]["toggle_mode"] = (val == QtCore.Qt.Checked)
        save_config(self.state)

    def back_to_main(self):
        self.main_window.move(self.pos())
        self.main_window.show()
        self.hide()

    def recenter_current_reticle(self):
        preset = self.state["selected_preset"]
        self.state[f"{preset}_offset_x"] = 0
        self.state[f"{preset}_offset_y"] = 0
        save_config(self.state)

    # Per-reticle size/width
    def set_overall_size(self, v):
        preset = self.state["selected_preset"]
        self.state[f"{preset}_overall_size"] = v / 100.0
        save_config(self.state)

    def set_overall_width(self, v):
        preset = self.state["selected_preset"]
        self.state[f"{preset}_overall_width"] = v / 100.0
        save_config(self.state)

    # Rifle scope
    def set_rifle_circle_color(self, col): self.state["rifle_circle_color"] = col; save_config(self.state)
    def set_rifle_circle_radius(self, v): self.state["rifle_circle_radius"] = v; save_config(self.state)
    def set_rifle_circle_width(self, v): self.state["rifle_circle_width"] = v; save_config(self.state)
    def set_rifle_cross_color(self, col): self.state["rifle_cross_color"] = col; save_config(self.state)
    def set_rifle_cross_length(self, v): self.state["rifle_cross_length"] = v; save_config(self.state)
    def set_rifle_cross_thickness(self, v): self.state["rifle_cross_thickness"] = v; save_config(self.state)
    def set_rifle_center_dot_color(self, col): self.state["rifle_center_dot_color"] = col; save_config(self.state)
    def set_rifle_center_dot_radius(self, v): self.state["rifle_center_dot_radius"] = v; save_config(self.state)

    # Rifle2
    def set_rifle2_circle_color(self, col): self.state["rifle2_circle_color"] = col; save_config(self.state)
    def set_rifle2_circle_radius(self, v): self.state["rifle2_circle_radius"] = v; save_config(self.state)
    def set_rifle2_circle_width(self, v): self.state["rifle2_circle_width"] = v; save_config(self.state)
    def set_rifle2_cross_color(self, col): self.state["rifle2_cross_color"] = col; save_config(self.state)
    def set_rifle2_cross_length(self, v): self.state["rifle2_cross_length"] = v; save_config(self.state)
    def set_rifle2_cross_thickness(self, v): self.state["rifle2_cross_thickness"] = v; save_config(self.state)
    def set_rifle2_center_dot_color(self, col): self.state["rifle2_center_dot_color"] = col; save_config(self.state)
    def set_rifle2_center_dot_radius(self, v): self.state["rifle2_center_dot_radius"] = v; save_config(self.state)
    def set_rifle2_elevation_lines(self, v): self.state["rifle2_elevation_lines"] = v; save_config(self.state)
    def set_rifle2_elevation_spacing(self, v): self.state["rifle2_elevation_spacing"] = v; save_config(self.state)
    def set_rifle2_elevation_length(self, v): self.state["rifle2_elevation_length"] = v; save_config(self.state)
    def set_rifle2_wind_lines(self, v): self.state["rifle2_wind_lines"] = v; save_config(self.state)
    def set_rifle2_wind_spacing(self, v): self.state["rifle2_wind_spacing"] = v; save_config(self.state)
    def set_rifle2_wind_length(self, v): self.state["rifle2_wind_length"] = v; save_config(self.state)
    def set_rifle2_wind_height(self, v): self.state["rifle2_wind_height"] = v; save_config(self.state)
    def set_rifle2_wind_side(self, v): self.state["rifle2_wind_side"] = v; save_config(self.state)

    # Dot
    def set_dot_color(self, col): self.state["dot_color"] = col; save_config(self.state)
    def set_dot_radius(self, v): self.state["dot_radius"] = v; save_config(self.state)

    # Cross
    def set_cross_color(self, col): self.state["cross_color"] = col; save_config(self.state)
    def set_cross_length(self, v): self.state["cross_length"] = v; save_config(self.state)
    def set_cross_thickness(self, v): self.state["cross_thickness"] = v; save_config(self.state)

    # Circle
    def set_circle_color(self, col): self.state["circle_color"] = col; save_config(self.state)
    def set_circle_radius(self, v): self.state["circle_radius"] = v; save_config(self.state)
    def set_circle_width(self, v): self.state["circle_width"] = v; save_config(self.state)

    # Chevron
    def set_chevron_color(self, col): self.state["chevron_color"] = col; save_config(self.state)
    def set_chevron_size(self, v): self.state["chevron_size"] = v; save_config(self.state)
    def set_chevron_thickness(self, v): self.state["chevron_thickness"] = v; save_config(self.state)

    def set_menu_opacity(self, opacity):
        opacity = float(opacity)
        self.setWindowOpacity(opacity)