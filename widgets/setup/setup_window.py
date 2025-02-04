from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
import datetime as dt
import email_validator
import hashlib
import smtplib
import secrets
import json

import widgets.setup.signin_widget as signin_widget
import widgets.setup.login_widget as login_widget
import widgets.setup.success_window as success_window

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle("Setup")
        self.setWindowIcon(QtGui.QIcon("assets/logo.png"))

        # Apply stylesheets
        qss = "widgets/setup/stylesheets/setup_window_styles.qss"
        with open(qss, "r") as f:
            self.setStyleSheet(f.read())

        setupmainstyles = "widgets/setup/stylesheets/setupGeneralStyles.qss"
        with open(setupmainstyles, "r") as f:
            self.setStyleSheet(self.styleSheet() + f.read())

        # Set window flags to include min/max buttons
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinMaxButtonsHint)

        # Set initial window state to maximized (full screen)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Create a QVBoxLayout for the dialog
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align the contents
        self.setLayout(self.layout)

        self.confirmation_code_str = ""  # Initialize confirmation_code_str as an instance variable

        self.signin_widget = signin_widget.SignInWidget()
        self.signin_widget.setObjectName("signin-widget")
        self.signin_widget.signup_button.clicked.connect(self.signup)
        self.signin_widget.confirm_input.returnPressed.connect(self.signup)
        self.signin_widget.login_instead_button.clicked.connect(self.switch_to_login)

        self.login_widget = login_widget.LoginWidget()
        self.login_widget.setObjectName("login-widget")
        self.login_widget.login_button.clicked.connect(self.login)
        self.login_widget.password_input.returnPressed.connect(self.login)
        self.login_widget.signup_instead_button.clicked.connect(self.switch_to_signup)

        # Add a QWidget as a container for centering
        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Initially add the login widget to the center layout
        self.center_layout.addWidget(self.login_widget)
        self.layout.addWidget(self.center_widget)

        # Frame for error labels when putting invalid data into input fields
        self.error_box = QWidget()
        self.error_box.layout = QVBoxLayout()
        self.error_box.setLayout(self.error_box.layout)
        self.layout.addWidget(self.error_box)

    def signup(self):
        email = self.signin_widget.email_input.text().lower()
        password = self.signin_widget.password_input.text()
        confirm_password = self.signin_widget.confirm_input.text()

        is_valid = True

        # Checks if email is valid using email-validator package (pip install email-validator)
        try:
            emailinfo = email_validator.validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except email_validator.EmailNotValidError as e:
            is_valid = False
            self.show_error("Email is invalid.")
            print("Email is invalid.")

        if len(password) < 6:
            is_valid = False
            self.show_error("Password must be at least 6 characters.")
            print("Password is too short.")

        if password != confirm_password:
            is_valid = False
            self.show_error("Passwords do not match.")
            print("Passwords do not match.")

        # runs if data has passed all other checks, and is formatted correctly
        if is_valid:
            print("Data is valid, proceeding with signup.")

            # Generate a random 12-character password with uppercase letters
            characters = "ABCDEFGHJKLMNPQRSTUVWXYZ123456789"  # Excludes 'O', 'o', '0'
            generated_password = ''.join(secrets.choice(characters) for i in range(12))

            # Use this generated password instead
            password_to_send = generated_password

            # Generate a random salt
            salt = secrets.token_hex(16) # 16 bytes for a secure salt

            # Combine the password and salt before hashing
            salted_password = password_to_send + salt

            # Hash the password with salt using SHA-256
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

            # Store email, salt, and hashed password securely (e.g., in a file)
            try:
                # open json file to get data dict
                with open("local_storage/logins/user_logins.json", "r") as f:
                    current_data = json.load(f)

                # check if email already exists
                try:
                    if current_data['data'].get(email):
                        is_valid = False
                        self.show_error("Email already in use")
                        print("Email already in use.")
                except KeyError:
                    new_data = {"data": { email: {
                    "salt": salt,
                    "hashed_password": hashed_password
                            }
                        }
                    }
                    # merge old data with new data
                    current_data["data"] = current_data["data"] | new_data["data"]

            # create new data if no old data
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                current_data = {"data": { email: {
                    "salt": salt,
                    "hashed_password": hashed_password
                        }
                    }
                }

        if is_valid:
            # Your email credentials
            sender_email = "noreply.informationassistant@gmail.com"
            sender_password = "inewptafzoguzxhv"

            # Email server configuration (for Gmail with TLS)
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.ehlo()
            connection.starttls()

            try:
                connection.ehlo()
                connection.login(user=sender_email, password=sender_password)

                # Create message
                subject = "DailyMailer Password"
                body = f"Thank you for registering with the DailyMailer. Your password is: {password_to_send}\n\nPlease keep it safe."

                # Specify sender and recipient email addresses in the 'msg' parameter
                message = f"From: {sender_email}\nTo: {email}\nSubject: {subject}\n\n{body}"

                connection.sendmail(from_addr=sender_email,
                                    to_addrs=email,
                                    msg=message)
                print("Email sent successfully.")

            except smtplib.SMTPException as e:
                print("Error sending email:", str(e))

            finally:
                connection.close()

            # Open the success dialog with email and password
            success_dialog = success_window.SuccessDialog(email, password_to_send)
            success_dialog.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            print("Opening success dialog.")
            # if success dialog was accepted, save data and proceed to program
            if success_dialog.exec() == QDialog.DialogCode.Accepted:
                # save login info and session info into client
                with open("local_storage/logins/user_logins.json", "w") as f:
                    json.dump(current_data, f, indent=4)
                self.save_last_login(email)
                self.accept()
                print("Signup process completed successfully.")
            else:
                print("Success dialog was not accepted.")

    def login(self):
        email = self.login_widget.email_input.text().lower()
        password = self.login_widget.password_input.text()

        # Load saved user data from file
        try:
            with open("local_storage/logins/user_logins.json") as f:
                user_logins = json.load(f)
                # check if email exists
                try:
                    user_info = user_logins["data"][email]
                    salt = user_info["salt"]
                    stored_hashed_password = user_info["hashed_password"]
                    
                    # Hash the entered password w/ salt for comparison
                    salted_password = password + salt
                    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
                    if hashed_password == stored_hashed_password:
                        self.save_last_login(email)
                        self.accept()
                        return
                except KeyError:
                    self.show_error("Email not found! Sign Up Instead")
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.show_error("Email not found")

        # If no match is found
        self.show_error("Invalid login credentials")

    def show_error(self, message):
        # show only 1 error at a time
        if self.error_box.layout.count() == 0:
            error_label = QLabel(f"<font color='red'>{message}</font>")
            error_label.setProperty("class", "error-label")
            self.error_box.layout.insertWidget(0, error_label)

            # Schedule clearing the error after 3 seconds
            error_timer = QtCore.QTimer(self)
            error_timer.setSingleShot(True)
            error_timer.timeout.connect(lambda: error_label.setParent(None))
            error_timer.start(3000)

    def switch_to_login(self):
        # clears layout and errors and switches to the login layout
        self.clear_layout()
        self.center_layout.addWidget(self.login_widget)
        try:
            self.error_box.layout.itemAt(0).widget().setParent(None)
        except AttributeError:
            pass
        self.layout.addWidget(self.error_box)

    def switch_to_signup(self):
        # clears layout and errors and switches to the signin layout
        self.clear_layout()
        self.center_layout.addWidget(self.signin_widget)
        try:
            self.error_box.layout.itemAt(0).widget().setParent(None)
        except AttributeError:
            pass
        self.layout.addWidget(self.error_box)

    def clear_layout(self):
        for i in reversed(range(self.center_layout.count())):
            self.center_layout.itemAt(i).widget().setParent(None)

    def save_last_login(self, email):
        # save time of login and email into file
        date = dt.datetime.now().strftime("%d/%m/%Y")
        time = dt.datetime.now().strftime("%H:%M:%S %p")
        session_info = {
            "last_login" : {
                "email": email,
                "date": date,
                "time": time,
                }
        }

        with open("local_storage/logins/last_login_session.json", "w") as f:
            json.dump(session_info, f, indent=4)