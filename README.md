# DeepSeek Local Client

## Project Description

This project is a chat client built using the Tkinter library, named Ollama GUI Chat Client. It allows users to interact with the Ollama chat model and save chat history.

## Features

- Users can input messages and converse with the chat model.
- Supports streaming responses.
- Users can create new conversations by clicking a button, using a timestamp as the conversation name.
- Saves historical conversation names and corresponding chat records to the `chat_history.json` file.
- Supports theme switching and remembers the user's last selected theme.

## File Description

- `deepseek_chat_GUI.py`: Main program file, containing the GUI implementation of the chat client and interaction logic with the chat model.
- `style.py`: Style file, containing style definitions for different themes and theme switching logic.
- `chat_history.json`: File storing the chat history between users and the model.
- `selected_theme.json`: File storing the user's last selected theme.
- `README.md`: Project documentation, including features, usage methods, and other relevant information.
- `requirements.txt`: List of Python libraries required for the project.

## Usage

1. Ensure that the required Python libraries are installed. You can install dependencies using the following command:

    ```sh
    pip install -r requirements.txt
    ```

2. Run the `deepseek_chat_GUI.py` file to start the chat client:

    ```sh
    python deepseek_chat_GUI.py
    ```

3. Input messages in the interface to converse with the model.
4. Click the "New Conversation" button to create a new conversation and save the history.
5. Use the theme selection box to switch themes; the program will remember the user's last selected theme.

![image-20250202010100330](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010100330.png)

![image-20250202010127855](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010127855.png)

![image-20250202010148047](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010148047.png)

![image-20250202010201804](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010201804.png)

![image-20250202010218280](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202010218280.png)

![image-20250202101548866](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202101548866.png)

![image-20250202101606528](https://newblogimg.oss-cn-beijing.aliyuncs.com/2024/image-20250202101606528.png)

### Packaging into an Executable File

1. Install `PyInstaller`:

    ```sh
    pip install pyinstaller
    ```

2. Run the packaging script `build_exe.bat`:

    ```sh
    pyinstaller --onefile --windowed deepseek_chat_GUI.py
    ```

3. Find the generated `deepseek_chat_GUI.exe` file in the `dist` folder.
4. Double-click to run `deepseek_chat_GUI.exe`.

## Contributions

Any form of contribution is welcome! Please submit issues or pull requests to help improve this project.