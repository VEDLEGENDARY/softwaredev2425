from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtGui import *
from widgets.tabs import all_tabs
from widgets.setup import setup_window
import threading
import json
import sys
import requests, socket
import platform, psutil
import ctypes
import subprocess
import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPROUTIFY")

        global APP_ICON
        APP_ICON = QIcon("assets/app_icon.png")
        self.setWindowIcon(APP_ICON)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Check if setup is needed
        if not self.check_setup():
            sys.exit(0)  # Exit if setup is canceled

        self.tabs = all_tabs.Tabs()
        self.setCentralWidget(self.tabs)
        with open("widgets/custom_widget_styles/tabs.qss", 'r') as f:
            self.setStyleSheet(f.read())

        self.headers = {
            'Content-Type': 'application/json'
        }

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background-color: #0776b8; color: #ffffff;")
        self.statusBar.addWidget(self.tabs.file_name)

    def check_setup(self):
        try:
            # comparing date of last login to todays date, if same, open application w/o login prompt
            with open("local_storage/logins/last_login_session.json", "r") as f:
                session_info = json.load(f)

            date = session_info["last_login"]["date"]
            last_day = int(date.split("/")[0])
            this_day = int(datetime.datetime.now().strftime("%d"))

            if this_day - last_day == 0:
                return True
            else:
                setup = setup_window.SetupDialog()
                setup.move(self.rect().center())  # Center the dialog relative to MainWindow
                return setup.exec() == QDialog.DialogCode.Accepted

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            setup = setup_window.SetupDialog()
            setup.move(self.rect().center())  # Center the dialog relative to MainWindow
            return setup.exec() == QDialog.DialogCode.Accepted

    def get_new_hash(self, session):
        self.tabs.console_log("REQUESTING NEW HASH...")
        systemData = self.getSystemInfo()
        with session.post(all_tabs.baseUrl + "/getNewHash", headers=all_tabs.headers, data=json.dumps( {"systemData": systemData} )) as r:
            response = r.json()
            try:
                with open(all_tabs.SYSTEM_DATA_PATH, "w") as sysdata_file:
                    sysdata_dict = {}
                    sysdata_json = ({"data": {"systemData": systemData}})
                    sysdata_dict.update(sysdata_json)
                    json.dump(sysdata_dict, sysdata_file, indent=3)
                    self.tabs.console_log("SYSTEM DATA RECORDED")
            except:
                self.tabs.console_log("UNABLE TO RECORD SYSTEM DATA")

            if response['newHash']:
                self.tabs.console_log("NEW HASH RETRIEVED")
                try:
                    with open(all_tabs.CLIENT_DATA_PATH, "w") as write_file:
                        newHash = response['newHash']
                        client_data_dict = {}
                        client_data_json = {"data": {"clientData": {"hash": newHash, "version": "1.0"}}}
                        client_data_dict.update(client_data_json)
                        json.dump(client_data_dict, write_file, indent=3)
                        self.tabs.console_log("HASH SAVED")
                except:
                    self.tabs.console_log("ERROR: UNABLE TO SAVE HASH DATA")

            else:
                self.tabs.console_log("ERROR: HASH RETURN UNRECOGNIZED")

    # Calls back to the server to check if the hash the client has is valid
    def hash_callback(self, hash, clientVersion, session):
        # Server will return boolean value
        self.tabs.console_log('VALIDATING EXISTING HASH...')
        with session.post(all_tabs.baseUrl + "/verifyHash", headers=all_tabs.headers, data=json.dumps({"hash": hash, "clientVer": clientVersion})) as r:
            response = r.json()
            valid = response['hashValid']
            if valid:
                return True
            else:
                return False

    def verify_hash(self, session):
        self.tabs.console_log("LOADING HASH DATA...")
        try:
            with open(all_tabs.CLIENT_DATA_PATH, "r") as open_file:
                client_data = json.load(open_file)
                hash = client_data['data']['clientData']['hash']
                clientVersion = client_data['data']['clientData']['version']
                self.tabs.console_log('HASH DATA LOADED')
                if hash == "":
                    self.tabs.console_log("NO HASH SAVED")
                    self.get_new_hash(session)
                else:
                    hashValid = self.hash_callback(hash, clientVersion, session)
                    if hashValid:
                        self.tabs.console_log("EXISTING HASH VALID")
                        pass

                    else:
                        self.tabs.console_log("EXISTING HASH INVALID, GETTING NEW HASH")
                        self.get_new_hash(session)
                        
        except:
            self.tabs.console_log("UNABLE TO LOAD HASH DATA FROM STORAGE")
        
    def initialize(self):
        self.tabs.console_log("INITIALIZING...")
        session = requests.Session()
        with session:
            server_online = self.tabs.api_callback(session)
            if server_online:
                self.tabs.console_log("VERIFYING HASH...")
                self.verify_hash(session)
            else:
                pass


# Main function that runs the app and all of it's necessary functions
def run_app():
    print("====================================\n")
    # Tabs.console_log(message="APPLICATION STARTED")
    app = QApplication(sys.argv)
    ui = MainWindow()
    
    ui.show()
    threading.Thread(target=ui.initialize).start()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
