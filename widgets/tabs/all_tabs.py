from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Signal, Slot
from widgets import (debug_window, popup_window)
from datetime import datetime
from zipfile import ZipFile
from unidecode import unidecode
from threading import Thread
import threading
import json
import requests


full_payload = {}
is_saved = False
has_data = False
file_filter = "Daily Mailer Project File (*.dmail)"
file_name = ""

CONTACT_PATH = "local_storage/contacts.json"
API_CONFIG_PATH = "local_storage/temp/api.json"
CLIENT_DATA_PATH = "local_storage/userdata/clientData.json"
SYSTEM_DATA_PATH = "local_storage/userdata/systemData.json"

# baseUrl = "http://127.0.0.1:5000"
baseUrl = "http://172.20.10.2:5000"

headers = {"Content-Type":"application/json"} 
now = datetime.now()
timeExec = now.strftime('%m-%d-%Y %H:%M:%S')

try:
    with open(CONTACT_PATH) as open_file:
        contacts = json.load(open_file)
except json.decoder.JSONDecodeError:
    contacts = ""

class Tabs(QWidget):
    received_api = Signal(tuple)
    def __init__(self):
        super().__init__()
        with open("widgets/custom_widget_styles/tabs.qss", 'r') as f:
            self.setStyleSheet(f.read())

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())
        
        self.layout = QVBoxLayout()

        from widgets.tabs import custom_tab_bar
        self.tabs = custom_tab_bar.TabWidget()
        self.tabs.setStyleSheet("TabWidget::tab-bar {alignment: left;} QLabel {alignment: center}")
        self.popup_window = popup_window.PopupWindow()
        self.debug_window = debug_window.DebugWindow()

        ############################################################ DASHBOARD TAB ################################
        from widgets.tabs.tab1 import dashboard_tab
        self.tab1 = dashboard_tab.DashboardTab()
        self.tabs.addTab(self.tab1, "Dashboard")

        ############################################################## CONTACT TAB ##############################################################
        from widgets.tabs.tab2 import contact_tab
        self.tab2 = contact_tab.ContactsTab()
        self.tabs.addTab(self.tab2, "Crops")
        
        # No connection needed - the add functionality is now handled by the card click

        ################################################ API TAB ################################################
        from widgets.tabs.tab3 import api_tab
        self.tab3 = api_tab.APITab()
        self.tabs.addTab(self.tab3, "APIs")
    
        ############################################## FORMAT TAB ###################################################
        from widgets.tabs.tab4 import format_tab        
        self.tab4 = format_tab.FormatTab()
        self.tabs.addTab(self.tab4, "Message")

        self.tab4.get_info_btn.clicked.connect(self.get_info)
        self.tab4.show_draft_btn.clicked.connect(self.set_draft_window)

        ######################################### SELECT CONTACTS TAB ######################################
        from widgets.tabs.tab5 import send_tab    
        self.tab5 = send_tab.SendTab()
        self.tabs.addTab(self.tab5, "Send")

        self.tab5.send_email_btn.clicked.connect(self.send_email)

        ################################## FUNCTIONS ############################################################
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tabs.currentChanged.connect(self.reload_tabs)

        self.file_name = QLabel("File Not Saved")

    ######################################### DASHBOARD TAB FUNCTIONS ################################################

        self.received_api.connect(self.update_progress_bar)

    def get_full_payload(self):
        try:            
            with open(CLIENT_DATA_PATH, "r") as read_file:
                client_data = json.load(read_file)["data"]["clientData"]

            with ZipFile(file_name, 'r') as readFile:
                apis = json.loads(readFile.read('api_config.json'))

            global full_payload
            full_payload = {}
            param_payload = []
            api_num = 0
            
            with requests.Session() as session:
                self.popup_window.desc_lb.setText("Getting API data...")
                for api in range(len(apis)):
                    current_api = apis[f"api{api}"]
                    if current_api["isEnabled"]:

                        to_send = {}
                        to_send.update(
                            {"client_info": {
                                    "hash": client_data["hash"],
                                    "version": client_data["version"]
                                }
                            })
                        to_send.update({"dataType":current_api["dataType"]})
                        self.popup_window.api_lb.setText(f"Pulling {current_api['dataType']} info")

                        to_send_data = {}
                        to_send_data.update({"timeExec":timeExec})

                        emails = []
                        for email in current_api["recipients"].values():
                            emails.append(email)
                        to_send_data.update({"email":emails})

                        if current_api["config"] is not None:
                            to_send_data.update(current_api["config"])

                        to_send.update({"data": to_send_data})
                        payload = json.loads(self.sendConfigData(session, payload=to_send, type=current_api['name']))
                        if payload == "2":
                            print("True")

                        self.received_api.emit((api_num + 1, len(apis)))
                        
                        new_payload = []
                        for data in payload["return"]["data"]:
                            data_keys = list(data.keys())
                            data_value = list(data.values())

                            if len(data_keys) > 1:
                                for i in range(len(data_keys)):
                                    new_payload.append({f"{to_send['dataType']}:{data_keys[i]}":data_value[i]})
                                    
                            else: 
                                new_payload.append({f"{to_send['dataType']}:{data_keys[0]}":data_value[0]})

                        for param in new_payload:
                            param_payload.append(param)
                        full_payload.update({f"api{api_num}" : new_payload})
                        api_num += 1
                self.popup_window.api_lb.clear()
                self.popup_window.desc_lb.setText("Done!")
                self.tab4.help_window.load_params(param_payload)
                self.tab4.ai_writer_window.get_variables(param_payload)

                global has_data
                has_data = True
                QApplication.processEvents()
                return full_payload
                        
        except FileNotFoundError as e:
            self.console_log(e)
            return
        
    @Slot(tuple)
    def update_progress_bar(self, data):
        value, count = data
        self.popup_window.progress.setRange(0, count)
        self.popup_window.progress.setValue(value)

    def get_info(self):
        if is_saved:
            self.save_file()
            
        else:
            self.save_as_file()

        self.popup_window.reset_widget()
        self.popup_window.set_progress_lyt()
        self.popup_window.show()

        threading.Thread(target=self.get_full_payload).start()

    ################################################## CONTACT TAB FUNCTIONS ######################################################

    def edit_row(self):
        # Assuming `self.tab2` is the correct instance that contains `crop_table`
        selected_row = self.tab2.crop_table.currentRow()
        
        if selected_row >= 0:
            name = self.tab2.crop_table.item(selected_row, 0).text()
            variety = self.tab2.crop_table.item(selected_row, 1).text()
            crop_type = self.tab2.crop_table.item(selected_row, 2).text()
            seed_type = self.tab2.crop_table.item(selected_row, 3).text()
            
            # Populate the input fields with the current data
            self.tab2.add_crop_name_tb.setText(name)
            self.tab2.variety_dropdown.setCurrentText(variety)
            self.tab2.type_dropdown.setCurrentText(crop_type)
            self.tab2.seed_type_dropdown.setCurrentText(seed_type)
            
            # Set the index of the row being edited
            self.tab2.current_edit_row = selected_row

            # Optional: Clear any errors
            self.tab2.error_lb.clear()
        else:
            self.tab2.error_lb.setText("Please select a row to edit.")


    def remove_row(self):
        try:
            selected_row = self.tab2.crop_table.currentRow()
            name = self.tab2.crop_table.item(selected_row, 0).text()

            contact_list = self.tab5.contact_lists_wgt.contact_list

            for i in range(contact_list.count()):
                item = contact_list.item(i)
                if item is not None:
                    if item.text() == name:
                        index = contact_list.indexFromItem(item).row()
                        contact_list.takeItem(index)

            if selected_row >= 0:    
                self.console_log(f"row {selected_row + 1} removed")
                self.tab2.crop_table.removeRow(selected_row)
                self.tab2.crop_table.setCurrentCell(-1, -1)
        except AttributeError:
            pass

    def remove_all(self):
        self.confirm_window = QMessageBox(self)
        self.confirm_window.setWindowTitle("Confirm Remove")
        self.confirm_window.setText("Remove all contacts?")
        self.confirm_window.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.confirm_window.setIcon(QMessageBox.Icon.Question)
        button = self.confirm_window.exec()

        if button == QMessageBox.StandardButton.Yes:
            while self.tab2.crop_table.rowCount() > 0:
                self.tab2.crop_table.removeRow(0)
                
            self.tab5.contact_lists_wgt.contact_list.clear()

    ################################################## API TAB FUNCTIONS #################################################

    def save_api_dict(self):
        api_dict = {}
        for row in range(self.tab3.api_frame.layout.count()):
            current_api: self.tab3.api_widget.APIWidget = self.tab3.api_frame.layout.itemAt(row).widget()
            if current_api.has_config:
                
                api_name = current_api.json_name
                api_is_enabled = current_api.enable_cb.isChecked()
                api_config = current_api.config_window.config_dict
                self.tab5.contact_lists_wgt.apply()
                api_recipients = self.tab5.contact_lists_wgt.contacts

                api = {"name":api_name, "isEnabled":api_is_enabled, "config":api_config, "recipients":api_recipients, "dataType":current_api.dataType}
                api_dict.update({f"api{row}":api})
            else:
                api_name = current_api.json_name
                api_is_enabled = current_api.enable_cb.isChecked()
                self.tab5.contact_lists_wgt.apply()
                api_recipients = self.tab5.contact_lists_wgt.contacts

                api = {"name":api_name, "isEnabled":api_is_enabled, "config":None, "recipients":api_recipients, "dataType":current_api.dataType}
                api_dict.update({f"api{row}":api})
        return api_dict

    ################################################## FORMAT TAB FUNCTIONS #################################################

    def set_draft_window(self):
        if has_data:
            self.tab4.export_format_html(full_payload)
        else: 
            html = self.tab4.format_editor.editor.toHtml()
            self.tab4.draft_window.draft_text.setHtml(html)

        self.tab4.draft_window.show()

    ################################################### OTHER FUNCTIONS ####################################################

    def save_file(self):
        global is_saved
        if is_saved:
            api_dict = self.save_api_dict()
            contacts = self.tab2.save_contacts_dict()
            format_dict = self.tab4.save_format_dict()

            api_json = json.dumps(api_dict, indent=4)
            contact_json = json.dumps(contacts, indent=4)
            format_json = json.dumps(format_dict, indent=4)
            
            try:
                global file_name
                with ZipFile(file_name, 'w') as writeFile:
                    writeFile.writestr('api_config.json', api_json)
                    writeFile.writestr('contacts.json', contact_json)
                    writeFile.writestr('format.json', format_json)

                    is_saved = True
                    self.file_name.setText(f"Working on {file_name}")
            except FileNotFoundError:
                self.console_log("FILE NOT SELECTED, CANT BE SAVED")
                return
            
        else:
            self.save_as_file()

    def save_as_file(self):
        global is_saved
        api_dict = self.save_api_dict()
        contacts = self.tab2.save_contacts_dict()
        format_dict = self.tab4.save_format_dict()


        api_json = json.dumps(api_dict, indent=4)
        contact_json = json.dumps(contacts, indent=4)
        format_json = json.dumps(format_dict, indent=4)
        
        global file_name
        file_name = QFileDialog.getSaveFileName(self, "Save as File", filter=file_filter)[0]
        try:
            with ZipFile(file_name, 'w') as writeFile:
                writeFile.writestr('api_config.json', api_json)
                writeFile.writestr('contacts.json', contact_json)
                writeFile.writestr('format.json', format_json)

                is_saved = True
                self.file_name.setText(f"Working on {file_name}")
        except FileNotFoundError:
            self.console_log("FILE NOT SELECTED, CANT BE SAVED")
            return


    def open_file(self):
        global is_saved
        global file_name

        file_name = QFileDialog.getOpenFileName(self, "Open File", filter=file_filter)[0]
        try:
            with ZipFile(file_name, 'r') as readFile:
                contacts_json = json.loads(readFile.read('contacts.json'))
                api_json = json.loads(readFile.read('api_config.json'))
                format_json = json.loads(readFile.read('format.json'))
                is_saved = True

                self.tab3.set_api_default()
                while self.tab2.crop_table.rowCount() > 0:
                    self.tab2.crop_table.removeRow(0)
            
            for row in range(len(contacts_json)):
                self.tab2.crop_table.insertRow(row)
                self.tab2.crop_table.setItem(row, 0, QTableWidgetItem(contacts_json[f"contact{row}"]["name"]))
                self.tab2.crop_table.setItem(row, 1, QTableWidgetItem(contacts_json[f"contact{row}"]["email"]))
            self.console_log("CONTACT TABLE LOADED")

            with open("local_storage/temp/contacts.json", "w") as write_file:
                json.dump(contacts_json, write_file, indent=4)

            with open(API_CONFIG_PATH, "w") as write_file:
                json.dump(api_json, write_file, indent=4)

            with open("local_storage/temp/format.html", "w") as write_file:
                json.dump(unidecode(self.tab4.format_editor.editor.toHtml()), write_file, indent=4)

            for row in range(self.tab3.api_frame.layout.count()):
                current_api = self.tab3.api_frame.layout.itemAt(row).widget()
                self.console_log(f"API{row} LOADED")
                self.file_name.setText(f"Working on {file_name}")

            self.tab4.subject_tb.setText(format_json["subject"])
            self.tab4.format_editor.editor.setHtml(format_json["body"])
            self.console_log("FORMAT EDITOR LOADED")

            self.tab5.contact_lists_wgt.select_contact_list.clear()
            self.console_log("CONTACT SELECTION LISTS LOADED")

            global has_data
            has_data = False

        except FileNotFoundError:
            self.console_log("FILE NOT FOUND, CANT BE OPENED")

    def new_project(self):
        self.tab3.set_api_default()
        self.tab4.clear_all()
        while self.tab2.crop_table.rowCount() > 0:
            self.tab2.crop_table.removeRow(0)
        global is_saved
        is_saved = False

    def reload_tabs(self):
        contacts = self.tab2.save_contacts_dict()
        
        try:
            TEMP_CONTACT_PATH = "local_storage/temp/contacts.json"
            with open(TEMP_CONTACT_PATH, "w") as write_file:
                json.dump(contacts, write_file, indent=4)

            if has_data is False:
                with open("local_storage/temp/format.html", "w") as write_file:
                    json.dump(unidecode(self.tab4.format_editor.editor.toHtml()), write_file, indent=4)
            
        except PermissionError as error:
            self.console_log(str(error))
            
        self.tab5.contact_lists_wgt.reload()
        
    def send_email(self):
        if has_data is False:
            self.popup_window.reset_widget()
            self.popup_window.set_progress_lyt()
            self.popup_window.show()

            payload_thread = threading.Thread(target=(self.get_full_payload))
            payload_thread.start()
            payload_thread.join()

        self.tab4.export_format_html(full_payload)

        with open("local_storage/temp/format.html") as read_file:
            html = read_file.read()

        subject = self.tab4.subject_tb.text()
        if subject == "":
            subject = "Email from the Daily Mailer"

        with open("local_storage/temp/contacts.json") as read_file:
            contacts = json.load(read_file)

        name_email = {}
        for row in range(self.tab5.contact_lists_wgt.select_contact_list.count()):
            contact_info = contacts[f"contact{row}"]
            name = contact_info["name"]
            email = contact_info["email"]

            name_email.update({name:email})

        recipients = []
        for i in range(self.tab5.contact_lists_wgt.contact_list.count()):
            name = self.tab5.contact_lists_wgt.contact_list.item(i).text()
            if name in name_email:
                recipients.append(name_email[name])

        self.popup_window.reset_widget()
        self.popup_window.set_sending_html_lyt()
        self.popup_window.setWindowTitle("Sending...")
        self.popup_window.desc_lb.setText("Emailing HTML data to recipients...")
        self.popup_window.show()

        if recipients == []:
            
            self.console_log("RECIPIENT LIST IS EMPTY")
            return None

        with requests.Session() as session:
            self.sendHTMLData(html, subject, recipients, session)

    def console_log(self, message: str):
        global log_time, log_date

        now = datetime.now()
        log_date = now.strftime("%m/%d/%Y")
        log_time = now.strftime("%I:%M:%S %p")

        print(f"{log_time} | {message}")
        self.debug_window.debug_list.addItem(f"{log_time} | {message}")

    ############################################ BACKEND FUNCTIONS ###########################################

    def sendConfigData(self, session, payload, type):
        if self.api_callback(session):
            pass

        else:
            self.console_log("API UNAVAILABLE AT THIS TIME; PAYLOAD ABORTING")
            return

        self.console_log("SENDING CONFIG DATA...")

        try:
            configdata = json.dumps(payload)
            with session.post(baseUrl + "/configData", headers=headers, data=configdata) as r:
                response = r.json()
                respCode = response['code']
                # Return code = 1 means error
                # Return code = 2 means invalid hash
                if respCode == 0:
                    self.console_log(f"{type} DATA UPLOADED SUCCESSFULLY")
                    return r.text
                elif respCode == 2:
                    self.console_log(f"ERROR UPLOADING DATA TO SERVER - INVALID CLIENT HASH")
                    return str(2)

                else:
                    self.console_log("ERROR UPLOADING DATA TO SERVER - UNKNOWN SERVER RESPONSE")  
                    return str(1)
        except:
            self.console_log(f"ERROR UPLOADING DATA TO SERVER - {type} REQUEST FAILED")
            return str(1)

    def sendHTMLData(self, html, subject, recipients, session):
        def send():
            if self.api_callback(session=requests.Session()):
                pass
            else:
                self.console_log("API UNAVAILABLE AT THIS TIME; PAYLOAD ABORTING")
                return

            self.console_log("SENDING HTML TO BE EMAILED...")

            with open(CLIENT_DATA_PATH, "r") as read_file:
                client_data = json.load(read_file)["data"]["clientData"]

            payload = json.dumps({
                "client_info": {
                    "hash": client_data["hash"],
                    "version": client_data["version"],
                },
                "dataType": "HTML Data",

                "data": {
                    "email": recipients,
                    "timeExec": timeExec,
                    "htmlData": html,
                    "subject": subject,
                }
            })

            r = session.post(baseUrl + "/submitHtml", headers=headers, data=payload)
            response = r.json()
            if response['code'] == 0:
                self.console_log("HTML DATA UPLOADED SUCCESSFULLY")
                self.popup_window.desc_lb.setText("Emails sent successfully.")
                self.popup_window.desc_lb.setWindowTitle("Success!")

            elif response['code'] == 2:
                self.console_log("FAILED TO UPLOAD HTML DATA - INVALID CLIENT HASH")
                self.popup_window.desc_lb.setText("Unable to send emails.\n[Code 2]: Invalid Client Hash")

            else:
                self.console_log("FAILED TO UPLOAD HTML DATA")
                self.popup_window.desc_lb.setText("Unable to send emails.")
                print(response)
    
        Thread(target=send).start()

    def display_callback_error(self, args: str):
        self.popup_window.set_server_unavailable_lyt()
        self.popup_window.show()
        self.popup_window.desc_lb.setText(args)

    # Function that sends layout request back to the API to make sure it is online.
    def api_callback(self, session):
        self.console_log("PINGING SERVER...")
        try:
            with session.get(baseUrl + "/apiStatus", headers=headers) as r:
                response = r.json()
                if response:
                    code = response['code']
                    if code == 0:
                        self.console_log("API OPERABLE")
                        return True
                    else:
                        self.console_log(f"API AT {baseUrl} IS INOPERABLE AT THIS TIME")
                        # self.display_callback_error(f"Backend at {baseUrl} is unavailable at this time.")
                        return False
                    
                else:
                    self.console_log("SERVER NOT FOUND")
                    # self.display_callback_error(f"Server at {baseUrl} could not be found \nor is not responding.")
                    return False

        except:
            self.console_log("SERVER NOT FOUND")
            # self.display_callback_error(f"Server at {baseUrl} could not be found \nor is not responding.")
            return False