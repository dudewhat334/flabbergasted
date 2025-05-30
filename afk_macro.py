import threading
import keyboard
import time
import random

class AFKMacro:
    def __init__(self, state):
        self.state = state
        self.afk_keys = ['w', 'a', 's', 'd']
        self.opp = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
        self.movement_history = []
        self.running = True
        self.phase = "move"  # Only relevant if return is enabled
        self.listen_thread = threading.Thread(target=self.listen_afk, daemon=True)
        self.listen_thread.start()

    def listen_afk(self):
        while self.running:
            if not self.state.get('afk_enabled', False):
                time.sleep(0.05)
                continue

            # User input disables and resets everything
            if any(keyboard.is_pressed(key) for key in self.afk_keys):
                self.state['afk_enabled'] = False
                self.movement_history.clear()
                self.phase = "move"
                continue

            interval = float(self.state.get('afk_move_interval', 1.0))
            move_duration = float(self.state.get('afk_move_amount', 0.01))

            # If return to home is enabled, use move/return phases
            if self.state.get('afk_return_home', False):
                if self.phase == "move":
                    chosen_key = random.choice(self.afk_keys)
                    print(f"[MOVE] Pressing {chosen_key} for {move_duration}s, then waiting {interval}s")
                    keyboard.press(chosen_key)
                    time.sleep(move_duration)
                    keyboard.release(chosen_key)
                    self.movement_history = [(chosen_key, move_duration)]
                    time.sleep(interval)
                    self.phase = "return"
                elif self.phase == "return":
                    if self.movement_history:
                        move, duration = self.movement_history[0]
                        opp_key = self.opp.get(move)
                        print(f"[RETURN] Pressing {opp_key} for {duration}s, then waiting {interval}s")
                        keyboard.press(opp_key)
                        time.sleep(duration)
                        keyboard.release(opp_key)
                        time.sleep(interval)
                    self.movement_history.clear()
                    self.phase = "move"
            else:
                # Only ever move randomly, never return
                chosen_key = random.choice(self.afk_keys)
                print(f"[MOVE ONLY] Pressing {chosen_key} for {move_duration}s, then waiting {interval}s")
                keyboard.press(chosen_key)
                time.sleep(move_duration)
                keyboard.release(chosen_key)
                time.sleep(interval)

    def stop(self):
        self.running = False