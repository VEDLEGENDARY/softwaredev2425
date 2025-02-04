from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import widgets.functions.gpt_interface as ai
import sys
from threading import Thread

TOKEN_LIMIT = 3000

# generate a short informal blue themed email giving students a short reading assignment based on the quote of the day. Also give them a short and concise weather report

class AIWriterWindow(QWidget):
    received = Signal(int)
    def __init__(self):
        super(AIWriterWindow, self).__init__()
        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.styles = f.read()
            self.setStyleSheet(self.styles)

        APP_ICON = QIcon("assets/app_icon.png")
        self.setWindowIcon(APP_ICON)

        self.setWindowTitle("AI Writer")
        self.setFixedSize(800, 600)
        self.layout = QGridLayout()
        self.setLayout(self.layout)


        self.info_lb = QLabel("Enter your prompt here:")
        self.info_lb.setStyleSheet("font-size: 20px")
        self.layout.addWidget(self.info_lb, 0, 0)
        self.info_lb.setObjectName("prompt_text")

        self.error_lb = QLabel("")
        self.error_lb.setStyleSheet("color: red")
        self.layout.addWidget(self.error_lb, 0, 1)

        self.prompt_editor = QTextEdit()
        self.prompt_editor.setMaximumHeight(100)
        self.prompt_editor.setAcceptRichText(False)
        self.layout.addWidget(self.prompt_editor, 1, 0, 1, 2)

        self.generate_lb = QLabel("Generated Email:")
        self.generate_lb.setStyleSheet("font-size: 20px")
        self.layout.addWidget(self.generate_lb, 2, 0, 1, 2)
        self.generate_lb.setObjectName("generate_text")

        self.draft_text = QTextEdit(self)
        self.draft_text.setAcceptRichText(True)
        self.draft_text.setReadOnly(True)
        self.layout.addWidget(self.draft_text, 3, 0, 1, 2)

        self.send_prompt_btn = QPushButton("Generate Email")
        self.send_prompt_btn.clicked.connect(self.send_prompt)
        self.layout.addWidget(self.send_prompt_btn, 4, 0)

        self.accept_btn = QPushButton("Accept Email")
        self.layout.addWidget(self.accept_btn, 4, 1)

        self.response = ""
        self.variables = []
        self.in_progress_window = QMessageBox(QMessageBox.Icon.NoIcon, "Processing Request...", "Generating response...")
        self.in_progress_window.setStyleSheet(self.styles)
        self.in_progress_window.setText("Getting AI response...")

        self.received.connect(self.when_received)

    def when_received(self):
        self.in_progress_window.close()
        try:
            self.draft_text.setText(self.response)
        except Exception as e:
            error = str(e)
            self.draft_text.setPlainText(error)

    def send_prompt(self):
        prompt = self.prompt_editor.toPlainText()
        if prompt == "":
            self.error_lb.setText("Please enter a prompt.")
            self.empty_error()
            return
        
        self.in_progress_window.show()
        QApplication.processEvents()

        def get():
            self.response = ai.get_gpt_response(prompt, self.variables, TOKEN_LIMIT)
            self.received.emit(0)

        Thread(target=get).start()

    def empty_error(self):
        QTimer().singleShot(2000, lambda: self.error_lb.setText(""))

    def get_variables(self, payload):
        self.variables = []
        for setting in payload:
            self.variables.append(f"{{{list(setting.keys())[0]}}}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AIWriterWindow()
    window.show()
    app.exec()