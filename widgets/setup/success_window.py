from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui

class SuccessDialog(QDialog):
    def __init__(self, username, confirmation_code):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("assets/app_icon.png"))
        self.setWindowTitle("Verify Email")
        self.setGeometry(300, 250, 300, 200)

        qss = "widgets/setup/stylesheets/success-window-styles.qss"
        with open(qss, "r") as f:
            self.setStyleSheet(f.read())

        setupmainstyles = "widgets/setup/stylesheets/setupGeneralStyles.qss"
        with open(setupmainstyles, "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username = username
        self.confirmation_code = confirmation_code

        self.info_label = QLabel("Verify Email")
        self.info_label.setProperty("class", "info-label")
        self.layout.addWidget(self.info_label)

        self.username_label = QLabel(f"Email: {self.username}")
        self.username_label.setProperty("class", "input-label")
        self.layout.addWidget(self.username_label)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter the 12 digit code sent to your email for verification.")
        self.layout.addWidget(self.code_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.check_code)
        self.ok_button.setObjectName("ok-button")
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.trials = 0  # Initialize the trials counter as an instance variable

    def check_code(self):
        self.trials += 1  # Increment the trials counter
        if self.code_input.text() == self.confirmation_code:
            if self.trials < 6:
                self.accept()
            else:
                self.too_many_tries()
                error_timer = QtCore.QTimer(self)
                error_timer.setSingleShot(True)
                error_timer.timeout.connect(self.close)  # Close the dialog
                error_timer.start(10000)
        else:
            self.show_error()
            error_timer = QtCore.QTimer(self)
            error_timer.setSingleShot(True)
            error_timer.timeout.connect(self.error_end)
            error_timer.start(5000)

    def too_many_tries(self):
        self.code_input.setStyleSheet("background-color: rgb(255, 172, 172)")
        self.code_input.setPlaceholderText("Too many invalid tries. Resend verification code after checking email.")

    def show_error(self):
        self.code_input.setStyleSheet("background-color: rgb(255, 172, 172)")
        self.code_input.setPlaceholderText("Invalid Code")

    def error_end(self):
        self.code_input.setStyleSheet("background-color: rgb(248, 248, 255);")
        self.code_input.setPlaceholderText("Enter your 12 digit confirmation code.")