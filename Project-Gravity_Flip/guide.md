🧪 Step-by-Step: Run Your Pygame Game on Windows
1. ✅ Install Python (if not already)
    Go to https://www.python.org/downloads/windows
    Download the latest version (e.g., Python 3.12)
    During installation, check the box that says “Add Python to PATH”

2. 📁 Create Your Game Folder
    Put your game file (e.g., gravity_run.py) and any assets (like sprite images) into a folder like:
    ```Code
      C:\Users\YourName\Documents\GravityRunGame
    ```
3. 🧰 Open Command Prompt
    Press Win + R, type cmd, and hit Enter.
    Navigate to your game folder:
    ```bash
        cd C:\Users\YourName\Documents\GravityRunGame
    ```
4. 🧪 Create a Virtual Environment (optional but recommended)
    ```bash
     python -m venv venv
     venv\Scripts\activate
    ```
5. 📦 Install Pygame
    ```bash
        pip install pygame
    ```
6. 🚀 Run Your Game
    ```bash
        python gravity_run.py
    ```
    Your game window should open and start running!

🧠 Tips
If you use sprite images, make sure they’re in the same folder or correctly referenced.
You can also run the game from VS Code or IDLE by opening the .py file and pressing Run.
