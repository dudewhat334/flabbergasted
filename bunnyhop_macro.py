import threading
import keyboard
import time

class BunnyHopMacro:
    def __init__(self, state, macro_key='space', jump_key='space'):
        self.state = state
        self.macro_key = macro_key
        self.jump_key = jump_key
        threading.Thread(target=self.listen_bhop, daemon=True).start()

    def listen_bhop(self):
        while True:
            if self.state.get('bunnyhop_enabled', False) and keyboard.is_pressed(self.macro_key):
                interval = self.state.get('bunnyhop_interval', 40) / 1000
                keyboard.press_and_release(self.jump_key)
                time.sleep(interval)
            else:
                time.sleep(0.05)