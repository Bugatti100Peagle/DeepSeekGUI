import tkinter as tk
from tkinter import ttk

# 导入所有主题文件
from themes import spring_apricot_yellow_theme
from themes import moon_palace_blue_theme
from themes import heavenly_white_theme
from themes import crab_shell_blue_theme
from themes import chinese_red_theme
from themes import landscape_green_theme
from themes import morning_glory_purple_theme

import json
import os

# 主题字典
themes = {
    "春杏黄": spring_apricot_yellow_theme.apply_styles,
    "月宫蓝": moon_palace_blue_theme.apply_styles,
    "天汉白": heavenly_white_theme.apply_styles,
    "蟹壳青": crab_shell_blue_theme.apply_styles,
    "中国红": chinese_red_theme.apply_styles,
    "山水绿": landscape_green_theme.apply_styles,
    "牵牛紫": morning_glory_purple_theme.apply_styles,
}

THEME_FILE = "selected_theme.json"

def apply_styles(master, widgets, theme_name="天汉白"):
    if theme_name in themes:
        themes[theme_name](master, widgets)
        save_selected_theme(theme_name)
    else:
        raise ValueError(f"Theme '{theme_name}' not found.")

def save_selected_theme(theme_name):
    with open(THEME_FILE, 'w', encoding='utf-8') as f:
        json.dump({"selected_theme": theme_name}, f, ensure_ascii=False, indent=4)

def load_selected_theme():
    if os.path.exists(THEME_FILE):
        with open(THEME_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("selected_theme", "天汉白")
    return "天汉白"