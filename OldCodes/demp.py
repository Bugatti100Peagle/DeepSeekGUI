'''
Description: 
Version: 
Autor: JingJing zjqvrwz2020@163.com 
Date: 2025-02-01 15:12:37
LastEditors: JingJing zjqvrwz2020@163.com m
LastEditTime: 2025-02-01 16:18:56
'''
import requests
import json

class OllamaChatClient:
    def __init__(self, model_name="deepseek-r1:1.5b"):
        self.base_url = "http://localhost:11434/api/chat"
        self.model_name = model_name
        self.chat_history = []

    def chat(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        
        try:
            data = {
                "model": self.model_name,
                "messages": self.chat_history,
                "stream": True  # 启用流式
            }

            with requests.post(
                self.base_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                stream=True
            ) as response:
                
                full_response = []
                print("\n助手：", end="", flush=True)
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if chunk.get("done"):
                            break
                        content = chunk["message"]["content"]
                        print(content, end="", flush=True)
                        full_response.append(content)
                
                # 保存完整回复到历史记录
                self.chat_history.append({
                    "role": "assistant",
                    "content": "".join(full_response)
                })
                
                return "".join(full_response)

        except Exception as e:
            return f"Request failed: {str(e)}"

def main():
    print("Ollama 聊天客户端（输入'exit'退出）")
    client = OllamaChatClient()
    
    while True:
        user_input = input("\n你：")
        
        if user_input.lower() == 'exit':
            print("再见！")
            break
            
        response = client.chat(user_input)
        print(f"\n助手：{response}")

if __name__ == "__main__":
    main()