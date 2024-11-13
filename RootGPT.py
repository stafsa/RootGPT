import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, QFrame
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
import sys

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
)
chat_session = model.start_chat()

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RootGPT")
        self.setGeometry(300, 100, 800, 600)
        self.history_file = "chat_history.txt"
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        self.setPalette(palette)

        main_layout = QHBoxLayout()
        chat_layout = QVBoxLayout()
        chat_layout.setSpacing(15)

        self.title = QLabel("RootGPT")
        self.title.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #BB86FC;")
        chat_layout.addWidget(self.title)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #333333;")
        chat_layout.addWidget(line)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
            }
        """)
        chat_layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: #FFFFFF;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #555555;
            }
            QLineEdit:focus {
                border: 1px solid #BB86FC;
            }
        """)
        input_layout.addWidget(self.user_input)

        self.delete_button = QPushButton("Delete History")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #BB86FC;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
        """)
        self.delete_button.clicked.connect(self.remove_chat_history)
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #BB86FC;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.delete_button)
        chat_layout.addLayout(input_layout)

        self.chat_data = {}
        self.current_chat_id = None

        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: #BB86FC;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 5px;
            }
        """)
        self.chat_list.setFixedWidth(200)
        self.chat_list.itemClicked.connect(self.load_chat)

        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.setStyleSheet("""
            QPushButton {
                background-color: #BB86FC;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9B6FCF;
            }
        """)
        self.new_chat_button.clicked.connect(self.new_chat)
        
        side_layout = QVBoxLayout()
        side_layout.addWidget(self.new_chat_button)
        side_layout.addWidget(self.chat_list)
        
        main_layout.addLayout(chat_layout)
        main_layout.addLayout(side_layout)
        
        self.setLayout(main_layout)
        
        self.load_chat_history()
        if not self.chat_data:
            self.new_chat()

    def new_chat(self):
        chat_id = f"Chat {len(self.chat_data) + 1}"
        self.chat_data[chat_id] = []
        self.current_chat_id = chat_id
        self.chat_list.addItem(QListWidgetItem(chat_id))
        self.chat_display.clear()

    def load_chat(self, item):
        self.current_chat_id = item.text()
        self.chat_display.clear()
        for sender, message in self.chat_data[self.current_chat_id]:
            color = "#BB86FC" if sender == "You" else "#03DAC5"
            self.chat_display.append(f"<span style='color:{color};'>{sender}:</span> {message}")

    def send_message(self):
        user_message = self.user_input.text().strip()
        if user_message:
            self.chat_display.append(f"<span style='color:#BB86FC;'>You:</span> {user_message}")
            self.chat_data[self.current_chat_id].append(("You", user_message))
            self.user_input.clear()
            self.save_chat_history()

            try:
                response = chat_session.send_message(user_message)
                model_message = response.text



                if self.is_code(model_message):
                    self.chat_display.append(f"```python\n{model_message}\n```")
                else:
                    self.chat_display.append(f"<span style='color:#03DAC5;'>RootGPT:</span> {model_message}\n")
                
                self.chat_data[self.current_chat_id].append(("RootGPT", model_message))
                self.save_chat_history()
            except Exception as e:
                self.chat_display.append(f"<span style='color:#FF0000;'>An error occured:</span> ```{str(e)}```\n")

    def remove_chat_history(self):
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            sys.exit()
    def save_chat_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.chat_data, f)

    def load_chat_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.chat_data = json.load(f)
            for chat_id in self.chat_data:
                self.chat_list.addItem(QListWidgetItem(chat_id))

    def is_code(self, message):
        keywords = ['def', 'class', 'import', 'for', 'if', 'else', 'return']
        return any(keyword in message for keyword in keywords)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
