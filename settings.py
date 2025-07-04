import json
import os
from pynput import keyboard
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "language": "ES",
            "audioBot":True
            }
        
        save_config(default_config)
        return default_config

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def get_language():
    return load_config().get("language")

def set_language(language):
    config = load_config()
    config["language"] = language
    save_config(config)


def set_audio_bot(audio_bot):
    config = load_config()
    config["audioBot"] = audio_bot
    save_config(config) 

def get_audio_bot():
    return load_config().get("audioBot")

def get_shortcuts():
    config = load_config()
    return {k: set(v) for k, v in config.get("shortcuts", {}).items()}

def set_shortcut(action, shortcut_str):
    config = load_config()
    keys = [key.strip().lower() for key in shortcut_str.split("+")]
    config["shortcuts"][action] = keys
    save_config(config)