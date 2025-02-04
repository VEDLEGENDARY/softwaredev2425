from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class FormatHelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formatting Help")
        self.setWindowIcon(QIcon("assets/help_icon.png"))
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        with open("widgets/custom_widget_styles/word_processor.qss", 'r') as f:
            self.setStyleSheet(f.read())

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.help_lb = QLabel("Copy and paste these variables into your email, they will be substituted with their values before being sent.", self)
        self.help_lb.setWordWrap(True)
        self.layout.addWidget(self.help_lb)

        self.param_list = QListWidget(self)
        
        self.param_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.param_list)

    def load_params(self, payload):
        self.param_list.clear()
        for setting in payload:
            self.param_list.addItem(f"{{{list(setting.keys())[0]}}}")
