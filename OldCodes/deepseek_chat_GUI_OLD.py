import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import queue
import requests
import json
import os
from datetime import datetime

HISTORY_FILE = "chat_history.json"

class OllamaChatClient:
    def __init__(self, model_name="deepseek-r1:1.5b"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
        self.chat_history = []

    def chat(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        
        try:
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True  # 启用流式传输
            }

            with requests.post(
                self.base_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                stream=True
            ) as response:
                if response.status_code != 200:
                    yield f"请求失败，状态码: {response.status_code}"
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if chunk.get("done"):
                            yield "\n"  # 在响应完成后添加换行符
                            break
                        if "response" in chunk:
                            yield chunk["response"]
                        else:
                            yield f"响应格式错误: {chunk}"
        
        except Exception as e:
            yield f"DeepSeek聊天API调用错误：{e}"

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.client = OllamaChatClient()
        self.response_queue = queue.Queue()
        self.history = self.load_history()
        self.current_conversation = None
        
        # 初始化界面
        self.setup_ui()
        # 启动队列检查
        self.master.after(100, self.process_queue)

    def setup_ui(self):
        self.master.title("Ollama Chat Client")
        
        # 左侧历史对话列表框
        self.history_listbox = tk.Listbox(self.master)
        self.history_listbox.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)
        self.load_history_to_listbox()
        
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.chat_display.tag_configure("user", foreground="blue")
        self.chat_display.tag_configure("bot", foreground="green")
        self.chat_display.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.entry = tk.Text(self.master, height=4)  # 使用Text小部件并设置高度为4行
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.on_enter_pressed)
        
        self.send_button = ttk.Button(self.master, text="发送", command=self.on_send_button_clicked)
        self.send_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # 添加控制框架
        control_frame = ttk.Frame(self.master)
        control_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        self.add_clear_button(control_frame)

        # 设置行列权重
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)

    def on_enter_pressed(self, event):
        self.send_message()
        return "break"  # 阻止Text小部件插入换行符

    def on_send_button_clicked(self):
        self.send_message()

    def send_message(self):
        message = self.entry.get("1.0", tk.END).strip()
        if message:
            self.chat_display.insert(tk.END, f"你: {message}\n", "user")
            self.entry.delete("1.0", tk.END)
            threading.Thread(target=self.get_response, args=(message,)).start()

    def get_response(self, message):
        for response in self.client.chat(message):
            self.response_queue.put(response)

    def process_queue(self):
        try:
            while True:
                response = self.response_queue.get_nowait()
                self.chat_display.insert(tk.END, response, "bot")
                self.chat_display.see(tk.END)  # 自动滚动到底部
        except queue.Empty:
            pass
        self.master.after(100, self.process_queue)

    def add_clear_button(self, control_frame):
        clear_btn = ttk.Button(
            control_frame,
            text="清空历史",
            command=self.clear_history
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

    def clear_history(self):
        self.client.chat_history = []
        self.chat_display.delete(1.0, tk.END)
        self.history_listbox.delete(0, tk.END)
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def load_history_to_listbox(self):
        for item in self.history:
            self.history_listbox.insert(tk.END, item["summary"])

    def on_history_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_conversation = self.history[index]
            self.chat_display.delete(1.0, tk.END)
            for message in self.current_conversation["messages"]:
                role = "user" if message["role"] == "user" else "bot"
                self.chat_display.insert(tk.END, f"{message['role']}: {message['content']}\n", role)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()