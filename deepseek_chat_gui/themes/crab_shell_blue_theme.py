from tkinter import ttk

def apply_styles(master, widgets):
    style = ttk.Style(master)
    style.theme_use("clam")

    # 主背景色（浅青）
    bg_color = "#e3f2fd"
    fg_color = "#1565c0"
    select_bg_color = "#1976d2"
    select_fg_color = "white"

    # 配置样式
    style.configure("TButton", padding=5, relief="flat", background="#1565c0", foreground="white")
    style.map("TButton", background=[("active", "#0d47a1")])
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TEntry", padding=5, fieldbackground="#ffffff", foreground=fg_color)
    style.configure("TCombobox", padding=5, fieldbackground="#ffffff", foreground=fg_color)
    style.configure("TFrame", background=bg_color)

    # 更新窗口背景色
    master.config(bg=bg_color)

    # 更新输入框、中间的框和左边的背景颜色
    widgets['entry'].config(bg=bg_color, fg=fg_color)
    widgets['stream_display'].config(bg=bg_color, fg=fg_color)
    widgets['history_listbox'].config(bg=bg_color, fg=fg_color, selectbackground=select_bg_color, selectforeground=select_fg_color)
    widgets['theme_combobox'].config(background=bg_color, foreground=fg_color)
    widgets['chat_display'].config(background=bg_color, foreground=fg_color)
