from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from widgets.tabs.tab5 import select_contacts_widget

class SendTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.contact_lists_wgt = select_contacts_widget.SelectContactsWidget()
        self.layout.addWidget(self.contact_lists_wgt, 0, 0)

        self.send_email_btn = QPushButton("Send Email to Recipients", self)
        self.send_email_btn.setMaximumWidth(350)
        self.send_email_btn.setStyleSheet("font-size: 25px;")
        self.layout.addWidget(self.send_email_btn, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
