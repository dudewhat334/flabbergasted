import threading
import pyautogui
import keyboard
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class MenuToggleController(QObject):
    request_toggle = pyqtSignal()

    def __init__(self, main_window, hotkey='f1'):
        super().__init__()
        self.main_window = main_window
        self.settings_window = main_window.settings_window
        self.redical_settings_window = main_window.redical_settings_window
        self.tools_window = main_window.tools_window  # Add the tools window
        self.menu_windows = [
            self.main_window,
            self.settings_window,
            self.redical_settings_window,
            self.tools_window  # Include tools window in the tracking list
        ]
        self.last_open_menu = self.main_window
        self.original_mouse_pos = None
        self.hotkey = hotkey
        self.request_toggle.connect(self.toggle_menu)
        for w in self.menu_windows:
            w.installEventFilter(self)
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    def eventFilter(self, obj, event):
        from PyQt5.QtCore import QEvent
        if event.type() == QEvent.Show:
            self.last_open_menu = obj
        return False

    def hotkey_listener(self):
        keyboard.add_hotkey(self.hotkey, self.emit_toggle)
        keyboard.wait()

    def emit_toggle(self):
        self.request_toggle.emit()

    def get_currently_open_menu(self):
        for w in self.menu_windows:
            if w.isVisible():
                return w
        return None

    def toggle_menu(self):
        current_menu = self.get_currently_open_menu()
        if current_menu:
            self.last_open_menu = current_menu
            current_menu.hide()
            # No need to move the mouse back since user requested it not to
            return
        self.open_and_focus_menu(self.last_open_menu)

    def open_and_focus_menu(self, menu):
        menu.show()
        menu.activateWindow()
        menu.raise_()
        self.original_mouse_pos = pyautogui.position()
        QTimer.singleShot(100, lambda: self.move_and_click_menu(menu))

    def move_and_click_menu(self, menu):
        x = menu.x() + menu.width() // 2
        y = menu.y() + 10
        pyautogui.moveTo(x, y)
        pyautogui.click()
        # No mouse move back