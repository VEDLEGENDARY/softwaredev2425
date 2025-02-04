from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QSizePolicy

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        setupmainstyles = "widgets/setup/stylesheets/setupGeneralStyles.qss"
        with open(setupmainstyles, "r") as f:
            self.setStyleSheet(f.read())

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Password input with show/hide toggle
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter 6 characters or more")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        # Toggle checkbox for password visibility
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.show_password_checkbox)

        self.login_button = QPushButton("Confirm Log In")
        self.login_button.setProperty("class", "confirm-button")
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.login_button)

        self.layout.addStretch(1)

        
        self.signup_instead_button = QPushButton("Sign Up Instead")
        self.signup_instead_button.setProperty("class", "instead-button")
        self.signup_instead_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.signup_instead_button)

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.signin_widget = SignInWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signin_widget)
        self.setLayout(self.layout)