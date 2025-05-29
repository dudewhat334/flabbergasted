import os
import json

ASSETS_DIR = "assets"
JSON_FILES = "Json-Files"
MENU_BACKGROUND_DIR = "Menu-Background"

BACKGROUND_PATH = os.path.join(ASSETS_DIR, MENU_BACKGROUND_DIR, "Capture.PNG")
JSON_DIR = os.path.join(ASSETS_DIR, JSON_FILES)
CONFIG_PATH = os.path.join(JSON_DIR, "sight_config.json")

os.makedirs(JSON_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "offset_x": 0,
    "offset_y": 0,
    "selected_preset": "rifle",
    "rifle_overall_size": 1.0,
    "rifle_overall_width": 1.0,
    "dot_overall_size": 1.0,
    "dot_overall_width": 1.0,
    "cross_overall_size": 1.0,
    "cross_overall_width": 1.0,
    "circle_overall_size": 1.0,
    "circle_overall_width": 1.0,
    "chevron_overall_size": 1.0,
    "chevron_overall_width": 1.0,

    # Rifle Scope (rifle)
    "rifle_circle_color": [0, 255, 0],
    "rifle_circle_radius": 100,
    "rifle_circle_width": 4,
    "rifle_cross_color": [0, 255, 0],
    "rifle_cross_thickness": 2,
    "rifle_cross_length": 60,
    "rifle_center_dot_color": [255, 0, 0],
    "rifle_center_dot_radius": 4,

    # Dot
    "dot_color": [255, 0, 0],
    "dot_radius": 8,

    # Cross
    "cross_color": [0, 255, 0],
    "cross_length": 40,
    "cross_thickness": 3,

    # Circle
    "circle_color": [0, 255, 255],
    "circle_radius": 40,
    "circle_width": 2,

    # Chevron
    "chevron_color": [255, 255, 0],
    "chevron_size": 24,
    "chevron_thickness": 3,

    "overlay_opacity": 1.0
}

PRESETS = {
    "rifle": "Rifle Scope",
    "rifle2": "Rifle Scope",
    "dot": "Dot",
    "cross": "Cross",
    "circle": "Circle",
    "chevron": "Chevron"
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        # Sanity-check: Ensure selected_preset is valid
        if config.get("selected_preset") not in PRESETS:
            config["selected_preset"] = list(PRESETS.keys())[0]
        return config
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)