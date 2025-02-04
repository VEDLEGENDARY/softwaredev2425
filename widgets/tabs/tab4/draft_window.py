from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

class DraftWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        with open("widgets/custom_widget_styles/word_processor.qss", 'r') as f:
            self.setStyleSheet(f.read())

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle("Draft Viewer")
        self.setWindowIcon(QIcon("assets/app_icon.png"))
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.draft_text = QTextEdit(self)
        self.draft_text.setAcceptRichText(True)
        self.draft_text.setReadOnly(True)
        self.layout.addWidget(self.draft_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DraftWindow()
    window.show()
    app.exec()