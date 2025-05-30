import sys
import pygame
from PyQt5 import QtWidgets
from gui_main import MainWindow
from crosshair_overlay import CrosshairOverlay
from menu_toggle_controller import MenuToggleController
from mouse_listener import start_rmb_listener
from config import load_config
from bunnyhop_macro import BunnyHopMacro
from afk_macro import AFKMacro  # <-- AFK Macro import

def main():
    pygame.init()
    info = pygame.display.Info()
    state = load_config()
    state.update({
        "screen_width": info.current_w,
        "screen_height": info.current_h,
        "overlay_visible": True,
        "app_running": True,
    })

    # Start Bunny Hop Macro
    bunnyhop_macro = BunnyHopMacro(
        state,
        macro_key=state.get('bunnyhop_macro_key', 'space'),
        jump_key=state.get('bunnyhop_jump_key', 'space')
    )

    # Start AFK Macro
    afk_macro = AFKMacro(state)

    # --- Start RMB listener ---
    rmb_listener = start_rmb_listener(state)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
        QLabel, QGroupBox, QSlider, QComboBox, QPushButton {
            color: white;
        }
        QGroupBox::title {
            color: white;
        }
    """)
    main_window = MainWindow(state)
    overlay = CrosshairOverlay(state)
    overlay.start()
    toggle_controller = MenuToggleController(main_window, hotkey='f1')
    main_window.show()
    app.exec_()
    state["app_running"] = False
    try:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    except Exception:
        pass
    overlay.wait()

if __name__ == "__main__":
    main()