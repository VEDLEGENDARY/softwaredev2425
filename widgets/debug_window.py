from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())
        self.setWindowTitle("Debug Panel")
        self.setWindowIcon(QIcon("assets/debug_icon.png"))
        self.setFixedSize(500, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.debug_list = QListWidget(self)
        self.layout.addWidget(self.debug_list)

        self.clear_btn = QPushButton("Clear Debug Output", self)
        self.clear_btn.clicked.connect(self.clear_debug_list)
        self.layout.addWidget(self.clear_btn)

    def clear_debug_list(self):
        self.debug_list.clear()