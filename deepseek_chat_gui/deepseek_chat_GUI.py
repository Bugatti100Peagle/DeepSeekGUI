import tkinter as tk
from tkinter import ttk, messagebox
from tkhtmlview import HTMLLabel
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
        self.dialogues = {}

        self.check_and_create_history_file()
        self.load_history()

    def check_and_create_history_file(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                self.dialogues = json.load(f)

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.dialogues, f, ensure_ascii=False, indent=4)

    def new_dialogue(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dialogues[timestamp] = []
        self.save_history()
        return timestamp

    def chat(self, prompt, dialogue_name):
        self.dialogues[dialogue_name].append({"role": "user", "content": prompt})
        self.save_history()

        try:
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True  # 启用流式传输
            }

            response_text = ""
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
                            response_text += chunk["response"]
                            yield chunk["response"]
                        else:
                            yield f"响应格式错误: {chunk}"

            response_text = self.remove_think_tags(response_text)
            self.dialogues[dialogue_name].append({"role": "bot", "content": response_text})
            self.save_history()

        except Exception as e:
            yield f"DeepSeek聊天API调用错误：{e}"

    def remove_think_tags(self, content):
        import re
        return re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)


class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.client = OllamaChatClient()
        self.response_queue = queue.Queue()
        self.history = self.client.dialogues
        self.current_conversation = None
        self.html_content = ""  # 用于存储当前显示的HTML内容

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

        self.chat_display = HTMLLabel(self.master, wrap=tk.WORD)
        self.chat_display.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.stream_display = tk.Text(self.master, height=8, wrap=tk.WORD)  # 用于流式输出展示模型输出内容
        self.stream_display.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        self.stream_display.config(state=tk.DISABLED)

        self.entry = tk.Text(self.master, height=4)  # 使用Text小部件并设置高度为4行
        self.entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.on_enter_pressed)

        self.send_button = ttk.Button(self.master, text="发送", command=self.on_send_button_clicked)
        self.send_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        # 添加控制框架
        control_frame = ttk.Frame(self.master)
        control_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        self.add_clear_button(control_frame)
        self.add_new_dialogue_button(control_frame)

        # 设置行列权重
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_rowconfigure(3, weight=0)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)

    def on_enter_pressed(self, event):
        if event.state & 0x4:  # 检测Ctrl键
            return  # 允许换行
        else:
            self.send_message()
            return "break"# 阻止Text小部件插入换行符

    def on_send_button_clicked(self):
        self.send_message()

    def send_message(self):
        if not self.current_conversation:
            self.new_dialogue()
        message = self.entry.get("1.0", tk.END).strip()
        if message and self.current_conversation:
            self.append_html(f"<p><b>你:</b> {message}</p>")
            self.entry.delete("1.0", tk.END)
            threading.Thread(target=self.get_response, args=(message,)).start()
            self.stream_display.config(state=tk.NORMAL)
            self.stream_display.delete(1.0, tk.END)
            self.stream_display.config(state=tk.DISABLED)

    def get_response(self, message):
        for response in self.client.chat(message, self.current_conversation):
            self.response_queue.put(response)

    def process_queue(self):
        try:
            while True:
                response = self.response_queue.get_nowait()
                self.stream_display.config(state=tk.NORMAL)
                self.stream_display.insert(tk.END, response)
                self.stream_display.config(state=tk.DISABLED)
                self.stream_display.see(tk.END)  # 自动滚动到底部
                if response == "\n":  # 回答完毕
                    content = self.stream_display.get("1.0", tk.END).strip()
                    content = self.remove_think_tags(content)
                    content = self.double_blank_lines(content)
                    self.append_html(f"<p><b>助手:</b> {content}</p>")
                    self.client.dialogues[self.current_conversation][-1]['content'] = content  # 更新历史记录
                    self.client.save_history()  # 保存更新后的历史记录
        except queue.Empty:
            pass
        self.master.after(100, self.process_queue)

    def remove_think_tags(self, content):
        import re
        return re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)

    def double_blank_lines(self, content):
        return content.replace("\n", "\n\n")

    def append_html(self, html):
        self.html_content += html
        self.chat_display.set_html(self.html_content)

    def add_clear_button(self, control_frame):
        clear_btn = ttk.Button(
            control_frame,
            text="清空历史",
            command=self.clear_history
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

    def add_new_dialogue_button(self, control_frame):
        new_dialogue_btn = ttk.Button(
            control_frame,
            text="新建对话",
            command=self.new_dialogue
        )
        new_dialogue_btn.pack(side=tk.LEFT, padx=5)

    def clear_history(self):
        self.client.dialogues = {}
        self.html_content = ""
        self.chat_display.set_html("")
        self.stream_display.config(state=tk.NORMAL)
        self.stream_display.delete(1.0, tk.END)
        self.stream_display.config(state=tk.DISABLED)
        self.history_listbox.delete(0, tk.END)
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        self.client.check_and_create_history_file()
        self.history = self.client.dialogues  # 更新历史记录
        self.new_dialogue()  # 清空历史后自动新建一个对话
        self.load_history_to_listbox()  # 更新对话列表

    def new_dialogue(self):
        dialogue_name = self.client.new_dialogue()
        self.history_listbox.insert(tk.END, dialogue_name)
        self.history_listbox.selection_clear(0, tk.END)
        self.history_listbox.selection_set(tk.END)
        self.current_conversation = dialogue_name
        self.html_content = ""
        self.chat_display.set_html("")
        self.stream_display.config(state=tk.NORMAL)
        self.stream_display.delete(1.0, tk.END)
        self.stream_display.config(state=tk.DISABLED)

    def load_history_to_listbox(self):
        self.history_listbox.delete(0, tk.END)  # 清空列表
        for dialogue_name in self.client.dialogues.keys():
            self.history_listbox.insert(tk.END, dialogue_name)  # 重新加载对话

    def on_history_select(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_conversation = self.history_listbox.get(index)
            self.html_content = ""
            self.chat_display.set_html("")
            if self.current_conversation in self.client.dialogues:
                for message in self.client.dialogues[self.current_conversation]:
                    role = "你" if message["role"] == "user" else "助手"
                    content = self.remove_think_tags(message['content'])
                    content = self.double_blank_lines(content)
                    self.append_html(f"<p><b>{role}:</b> {content}</p>")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()