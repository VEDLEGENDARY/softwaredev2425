from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class PopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon("assets/help_icon.png"))
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.layout.widget()

    def set_server_unavailable_lyt(self):
        self.setWindowTitle("Server Unavailable")
        self.desc_lb = QLabel(self)
        self.layout.addWidget(self.desc_lb, 0, 0, 1, 2)

        self.close_serverstatus_btn = QPushButton("Close App", self)
        self.close_serverstatus_btn.clicked.connect(QApplication.exit)
        self.layout.addWidget(self.close_serverstatus_btn, 1, 0)

        self.continue_btn = QPushButton("Continue Offline", self)
        self.continue_btn.clicked.connect(self.reset_widget)
        self.layout.addWidget(self.continue_btn, 1, 1)

    def set_sending_html_lyt(self):
        self.setWindowTitle("Sending Emails")
        self.desc_lb = QLabel(self)
        self.layout.addWidget(self.desc_lb, 0, 0)

        self.continue_btn = QPushButton("Close", self)
        self.continue_btn.clicked.connect(self.reset_widget)
        self.layout.addWidget(self.continue_btn, 1, 0)

    def set_progress_lyt(self):
        self.setWindowTitle("Getting Data")
        self.desc_lb = QLabel(self)
        self.layout.addWidget(self.desc_lb, 0, 0)

        self.api_lb = QLabel(self)
        self.layout.addWidget(self.api_lb, 1, 0)

        self.progress = QProgressBar(self)
        self.layout.addWidget(self.progress, 2, 0)

        self.close_progress_btn = QPushButton("Close", self)
        self.close_progress_btn.clicked.connect(self.reset_widget)
        self.layout.addWidget(self.close_progress_btn, 3, 0)

    def reset_widget(self):
        self.close()
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)