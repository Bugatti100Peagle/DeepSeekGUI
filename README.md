# DeepSeek本地客户端

## 项目描述

该项目是一个基于 Tkinter 库构建的聊天客户端，名为 Ollama GUI 聊天客户端。它允许用户与Ollama聊天模型进行交互，并保存聊天历史记录。

## 功能

- 用户可以输入消息并与聊天模型进行对话。
- 支持流式传输响应。
- 用户可以通过点击按钮新建对话，使用当前时间的时间戳作为对话名称。
- 保存历史对话名称和对应的聊天记录到 `chat_history.json` 文件中。
- 支持主题切换，并记忆用户上次选择的主题。

## 文件说明

- `deepseek_chat_GUI.py`：主程序文件，包含聊天客户端的 GUI 实现和与聊天模型的交互逻辑。
- `style.py`：样式文件，包含不同主题的样式定义和主题切换逻辑。
- `chat_history.json`：存储用户与模型之间的聊天历史记录的文件。
- `selected_theme.json`：存储用户上次选择的主题。
- `README.md`：项目文档，包含项目的功能、使用方法和其他相关信息。
- `requirements.txt`：项目依赖的 Python 库列表。

## 使用方法

1. 确保已安装所需的 Python 库。可以使用以下命令安装依赖：

    ```sh
    pip install -r requirements.txt
    ```

2. 运行 `deepseek_chat_GUI.py` 文件以启动聊天客户端：

    ```sh
    python deepseek_chat_GUI.py
    ```

3. 在界面中输入消息与模型进行对话。
4. 点击“新建对话”按钮以创建新的对话并保存历史记录。
5. 使用主题选择框切换主题，程序会记忆用户上次选择的主题。

![image-20250202010100330](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010100330.png)

![image-20250202010127855](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010127855.png)

![image-20250202010148047](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010148047.png)

![image-20250202010201804](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010201804.png)

![image-20250202010218280](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010218280.png)

![image-20250202101548866](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202101548866.png)

![image-20250202101606528](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202101606528.png)

### 打包成可执行文件

1. 安装 `PyInstaller`：

    ```sh
    pip install pyinstaller
    ```

2. 运行打包脚本 `build_exe.bat`：

    ```sh
    pyinstaller --onefile --windowed deepseek_chat_GUI.py
    ```

3. 在 `dist` 文件夹中找到生成的 `deepseek_chat_GUI.exe` 文件。
4. 双击运行 `deepseek_chat_GUI.exe`。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求以帮助改进该项目。
