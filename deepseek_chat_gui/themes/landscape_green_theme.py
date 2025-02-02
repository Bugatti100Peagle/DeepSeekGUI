from tkinter import ttk

def apply_styles(master, widgets):
    style = ttk.Style(master)
    style.theme_use("clam")

    # 主背景色（浅绿）
    bg_color = "#e0f2f1"  # 淡水绿
    fg_color = "#004d40"  # 深绿
    select_bg_color = "#00796b"  # 中等绿色
    select_fg_color = "white"  # 白色

    # 配置样式
    style.configure("TButton", padding=5, relief="flat", background="#00796b", foreground="white")
    style.map("TButton", background=[("active", "#00695c")])
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
