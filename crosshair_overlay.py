import pygame
import win32gui
import win32con
import ctypes
from PyQt5 import QtCore
from config import save_config, PRESETS

def get_windows_screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

class CrosshairOverlay(QtCore.QThread):
    def __init__(self, state):
        super().__init__()
        self.state = state

    def run(self):
        screen_w, screen_h = get_windows_screen_size()
        self.state["screen_width"] = screen_w
        self.state["screen_height"] = screen_h

        pygame.init()
        screen = pygame.display.set_mode(
            (screen_w, screen_h),
            pygame.NOFRAME
        )
        hwnd = pygame.display.get_wm_info()["window"]

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, 0, 0, screen_w, screen_h,
            win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW
        )
        win32gui.MoveWindow(hwnd, 0, 0, screen_w, screen_h, True)

        clock = pygame.time.Clock()
        while self.state["app_running"]:
            # --- TOGGLE & OPACITY LOGIC ---
            should_draw = False
            preset = self.state["selected_preset"]
            redicals = self.state.get("redicals", {})
            preset_settings = redicals.get(preset, {})
            rmb_down = self.state.get("_rmb_down", False)
            # Visibility logic: only control opacity, never what is drawn
            if preset_settings.get("always_on", False):
                should_draw = True
            elif preset_settings.get("toggle_mode", False) and rmb_down:
                should_draw = True

            # Set opacity: visible if should_draw and overlay_visible, else transparent
            if should_draw and self.state.get("overlay_visible", True):
                opacity = int(self.state.get("overlay_opacity", 1.0) * 255)
            else:
                opacity = 0

            win32gui.SetLayeredWindowAttributes(
                hwnd, 0x000000, opacity, win32con.LWA_ALPHA | win32con.LWA_COLORKEY
            )

            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state["app_running"] = False

            keys = pygame.key.get_pressed()
            changed = False

            offset_x_key = f"{preset}_offset_x"
            offset_y_key = f"{preset}_offset_y"
            offset_x = self.state.get(offset_x_key, 0)
            offset_y = self.state.get(offset_y_key, 0)

            if self.state.get("overlay_visible", True):
                if keys[pygame.K_UP]:
                    self.state[offset_y_key] = offset_y - 1
                    changed = True
                if keys[pygame.K_DOWN]:
                    self.state[offset_y_key] = offset_y + 1
                    changed = True
                if keys[pygame.K_LEFT]:
                    self.state[offset_x_key] = offset_x - 1
                    changed = True
                if keys[pygame.K_RIGHT]:
                    self.state[offset_x_key] = offset_x + 1
                    changed = True

            if changed:
                save_config(self.state)
                offset_x = self.state.get(offset_x_key, 0)
                offset_y = self.state.get(offset_y_key, 0)

            # Always draw the same crosshair (never a small/fallback version)
            # Opacity controls visibility, not what's drawn
            self.draw_crosshair(screen, offset_x, offset_y)

            pygame.display.update()
            clock.tick(60)
        pygame.quit()

    def draw_crosshair(self, screen, offset_x, offset_y):
        cx = self.state["screen_width"] // 2 + offset_x
        cy = self.state["screen_height"] // 2 + offset_y
        preset = self.state["selected_preset"]
        overall_size = self.state.get(f"{preset}_overall_size", 1.0)
        overall_width = self.state.get(f"{preset}_overall_width", 1.0)

        if preset == "rifle":
            pygame.draw.circle(
                screen,
                tuple(self.state["rifle_circle_color"]),
                (cx, cy),
                int(self.state["rifle_circle_radius"] * overall_size),
                max(1, int(self.state["rifle_circle_width"] * overall_width))
            )
            cross_len = int(self.state["rifle_cross_length"] * overall_size)
            cross_thick = max(1, int(self.state["rifle_cross_thickness"] * overall_width))
            cross_color = tuple(self.state["rifle_cross_color"])
            cross_bound = min(cross_len, int(self.state["rifle_circle_radius"] * overall_size))
            pygame.draw.line(screen, cross_color, (cx - cross_bound, cy), (cx + cross_bound, cy), cross_thick)
            pygame.draw.line(screen, cross_color, (cx, cy - cross_bound), (cx, cy + cross_bound), cross_thick)
            pygame.draw.circle(
                screen,
                tuple(self.state["rifle_center_dot_color"]),
                (cx, cy),
                max(1, int(self.state["rifle_center_dot_radius"] * overall_size)),
                0
            )
            pygame.draw.circle(
                screen,
                tuple(self.state["rifle_circle_color"]),
                (cx, cy),
                int(self.state["rifle_circle_radius"] * 0.5 * overall_size),
                max(1, int(self.state["rifle_circle_width"] * 0.5 * overall_width))
            )

        elif preset == "rifle2":
            circle_color = tuple(self.state["rifle2_circle_color"])
            circle_radius = int(self.state["rifle2_circle_radius"] * overall_size)
            circle_width = max(1, int(self.state["rifle2_circle_width"] * overall_width))
            pygame.draw.circle(screen, circle_color, (cx, cy), circle_radius, circle_width)
            cross_len = int(self.state["rifle2_cross_length"] * overall_size)
            cross_thick = max(1, int(self.state["rifle2_cross_thickness"] * overall_width))
            cross_color = tuple(self.state["rifle2_cross_color"])
            cross_bound = min(cross_len, circle_radius)
            pygame.draw.line(screen, cross_color, (cx - cross_bound, cy), (cx + cross_bound, cy), cross_thick)
            pygame.draw.line(screen, cross_color, (cx, cy - cross_bound), (cx, cy + cross_bound), cross_thick)
            pygame.draw.circle(
                screen,
                tuple(self.state["rifle2_center_dot_color"]),
                (cx, cy),
                max(1, int(self.state["rifle2_center_dot_radius"] * overall_size)),
                0
            )
            pygame.draw.circle(
                screen,
                circle_color,
                (cx, cy),
                int(circle_radius * 0.5),
                max(1, int(circle_width * 0.5))
            )
            elev_lines = self.state.get("rifle2_elevation_lines", 3)
            elev_spacing = int(self.state.get("rifle2_elevation_spacing", 25) * overall_size)
            elev_len = min(int(self.state.get("rifle2_elevation_length", 60) * overall_size), circle_radius * 2)
            for i in range(1, elev_lines + 1):
                y = cy + i * elev_spacing
                if y + cross_thick // 2 >= cy + circle_radius:
                    break
                pygame.draw.line(
                    screen,
                    cross_color,
                    (cx - elev_len // 2, y),
                    (cx + elev_len // 2, y),
                    cross_thick
                )
            wind_lines = self.state.get("rifle2_wind_lines", 2)
            wind_spacing = int(self.state.get("rifle2_wind_spacing", 25) * overall_size)
            wind_len = min(int(self.state.get("rifle2_wind_length", 40) * overall_size), circle_radius)
            wind_height = int(self.state.get("rifle2_wind_height", 25) * overall_size)
            wind_side = self.state.get("rifle2_wind_side", "left")
            y_wind = cy + wind_height
            for i in range(1, wind_lines + 1):
                dx = i * wind_spacing
                if wind_side in ("left", "both"):
                    left_x = cx - dx
                    if abs(left_x - cx) + wind_len // 2 < circle_radius:
                        pygame.draw.line(
                            screen, cross_color,
                            (left_x, y_wind - wind_len // 2),
                            (left_x, y_wind + wind_len // 2),
                            cross_thick
                        )
                if wind_side in ("right", "both"):
                    right_x = cx + dx
                    if abs(right_x - cx) + wind_len // 2 < circle_radius:
                        pygame.draw.line(
                            screen, cross_color,
                            (right_x, y_wind - wind_len // 2),
                            (right_x, y_wind + wind_len // 2),
                            cross_thick
                        )
        elif preset == "dot":
            pygame.draw.circle(
                screen,
                tuple(self.state["dot_color"]),
                (cx, cy),
                max(1, int(self.state["dot_radius"] * overall_size)),
                0
            )
        elif preset == "cross":
            length = int(self.state["cross_length"] * overall_size)
            thick = max(1, int(self.state["cross_thickness"] * overall_width))
            color = tuple(self.state["cross_color"])
            pygame.draw.line(screen, color, (cx - length, cy), (cx + length, cy), thick)
            pygame.draw.line(screen, color, (cx, cy - length), (cx, cy + length), thick)
        elif preset == "circle":
            pygame.draw.circle(
                screen,
                tuple(self.state["circle_color"]),
                (cx, cy),
                int(self.state["circle_radius"] * overall_size),
                max(1, int(self.state["circle_width"] * overall_width))
            )
        elif preset == "chevron":
            color = tuple(self.state["chevron_color"])
            size = int(self.state["chevron_size"] * overall_size)
            thick = max(1, int(self.state["chevron_thickness"] * overall_width))
            pygame.draw.line(screen, color, (cx - size, cy + size), (cx, cy - size), thick)
            pygame.draw.line(screen, color, (cx + size, cy + size), (cx, cy - size), thick)