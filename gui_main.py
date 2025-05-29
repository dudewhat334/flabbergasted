from PyQt5 import QtWidgets, QtGui, QtCore
from config import BACKGROUND_PATH
from gui_settings import SettingsWindow
from gui_redical import RedicalSettingsWindow
from gui_tools import ToolsWindow
# from overlay_window import OverlayWindow  # <-- REMOVED

class MainWindow(QtWidgets.QWidget):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowTitle("Crosshair Tool")
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
        self.title = QtWidgets.QLabel("CROSSHAIR TOOL", self)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title)

        btn_font = QtGui.QFont("Segoe UI", 10)
        btn_font.setItalic(True)
        green_btn_style = """
            color: green;
            background-color: black;
            border: 1px solid green;
        """

        self.settings_btn = QtWidgets.QPushButton("Settings")
        self.settings_btn.setFont(btn_font)
        self.settings_btn.setStyleSheet(green_btn_style)
        self.settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_btn)

        self.redical_settings_btn = QtWidgets.QPushButton("Redical Settings")
        self.redical_settings_btn.setFont(btn_font)
        self.redical_settings_btn.setStyleSheet(green_btn_style)
        self.redical_settings_btn.clicked.connect(self.open_redical_settings)
        layout.addWidget(self.redical_settings_btn)

        self.tools_btn = QtWidgets.QPushButton("Tools")
        self.tools_btn.setFont(btn_font)
        self.tools_btn.setStyleSheet(green_btn_style)
        self.tools_btn.clicked.connect(self.open_tools_menu)
        layout.addWidget(self.tools_btn)

        self.exit_btn = QtWidgets.QPushButton("Exit")
        self.exit_btn.setFont(btn_font)
        self.exit_btn.setStyleSheet(green_btn_style)
        self.exit_btn.clicked.connect(self.exit_app)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

        self.settings_window = SettingsWindow(self.state, self)
        self.redical_settings_window = RedicalSettingsWindow(self.state, self)
        self.tools_window = ToolsWindow(self.state, self)
        # --- REMOVED OverlayWindow creation ---
        # self.overlay_window = OverlayWindow(self.state)
        # self.overlay_window.show()
        self.set_opacity_all_menus(self.state.get("overlay_opacity", 1.0))

    def open_settings(self):
        self.settings_window.move(self.pos())
        self.settings_window.show()
        self.hide()

    def open_redical_settings(self):
        self.redical_settings_window.move(self.pos())
        self.redical_settings_window.show()
        self.hide()

    def open_tools_menu(self):
        self.tools_window.move(self.pos())
        self.tools_window.show()
        self.hide()

    def exit_app(self):
        self.state["app_running"] = False
        QtWidgets.QApplication.quit()

    def set_opacity_all_menus(self, opacity):
        self.setWindowOpacity(float(opacity))
        self.settings_window.set_menu_opacity(opacity)
        self.redical_settings_window.set_menu_opacity(opacity)
        self.tools_window.set_menu_opacity(opacity)