from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class SignInWidget(QWidget):
    def __init__(self):
        super().__init__()

        setupmainstyles = "widgets/setup/stylesheets/setupGeneralStyles.qss"
        with open(setupmainstyles, "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setMaximumSize(300, 400)

        self.email_label = QLabel("Email:")
        self.email_label.setProperty("class", "input-label")
        self.layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("name@example.com")
        self.layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:")
        self.password_label.setProperty("class", "input-label")
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter 6 characters or more")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.confirm_label = QLabel("Confirm Password:")
        self.confirm_label.setProperty("class", "input-label")
        self.layout.addWidget(self.confirm_label)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Must match previous password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.confirm_input)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.show_password_checkbox)

        self.signup_button = QPushButton("Confirm Sign Up")
        self.signup_button.setProperty("class", "confirm-button")
        self.layout.addWidget(self.signup_button)

        self.login_instead_button = QPushButton("Log In Instead")
        self.login_instead_button.setProperty("class", "instead-button")
        self.layout.addWidget(self.login_instead_button)

    def toggle_password_visibility(self):
        checked = self.show_password_checkbox.isChecked()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)

class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.signin_widget = SignInWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signin_widget)
        self.setLayout(self.layout)
