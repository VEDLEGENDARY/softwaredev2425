from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import json

CONTACT_PATH = "local_storage/contacts.json"

class SelectContactsWidget(QWidget):
    def __init__(self):
        super().__init__()

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())
            
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.descripton_lb = QLabel(f"Add contacts to receive the email", self)
        self.descripton_lb.setFont(QFont("Arial", 13, QFont.Bold))

        self.contact_error_lb = QLabel(self)
        self.contact_error_lb.setStyleSheet("color: red")

        self.add_contact_wgt = QWidget(self)
        self.add_contact_wgt.layout = QVBoxLayout()
        self.add_contact_wgt.setLayout(self.add_contact_wgt.layout)
        
        self.add_btn = QPushButton("Add Contact", self)
        self.add_btn.clicked.connect(self.add_contact)
        self.add_all_btn = QPushButton("Add All", self)
        self.add_all_btn.clicked.connect(self.add_all_contacts)

        self.add_contact_wgt.layout.addWidget(self.add_btn)
        self.add_contact_wgt.layout.addWidget(self.add_all_btn)

        self.remove_contact_wgt = QWidget(self)
        self.remove_contact_wgt.layout = QVBoxLayout()
        self.remove_contact_wgt.setLayout(self.remove_contact_wgt.layout)

        self.remove_btn = QPushButton("Remove Contact", self)
        self.remove_btn.clicked.connect(self.remove_contact)
        self.remove_all_btn = QPushButton("Remove All", self)
        self.remove_all_btn.clicked.connect(self.remove_all_contacts)

        self.remove_contact_wgt.layout.addWidget(self.remove_btn)
        self.remove_contact_wgt.layout.addWidget(self.remove_all_btn)

        self.select_contact_list = QListWidget(self)
        self.contact_list = QListWidget(self)

        self.layout.addWidget(self.descripton_lb, 0, 0)
        self.layout.addWidget(self.contact_error_lb, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(QLabel("Select contacts to be added", self), 1, 0)
        self.layout.addWidget(QLabel("Contacts which will receive the information", self), 1, 1)
        self.layout.addWidget(self.select_contact_list, 2, 0)
        self.layout.addWidget(self.contact_list, 2, 1)
        self.layout.addWidget(self.add_contact_wgt, 3, 0)
        self.layout.addWidget(self.remove_contact_wgt, 3, 1)

        self.contacts = {}

    def add_contact(self):
        try:
            contact_name = self.select_contact_list.currentItem().text()
            is_same = False

            for contact in range(self.contact_list.count()):
                if contact_name == self.contact_list.item(contact).text():
                    is_same = True
                
            if not is_same:
                self.contact_list.addItem(QListWidgetItem(contact_name))
                self.contact_error_lb.clear()
            else:
                self.contact_error_lb.setText("You cannot add the same contact more than once.")

        except AttributeError:
            self.contact_error_lb.setText("Please select a contact.")

    def add_all_contacts(self):
        self.contact_list.clear()
        for contact in range(self.select_contact_list.count()):
            contact_name = self.select_contact_list.item(contact).text()
            self.contact_list.addItem(QListWidgetItem(contact_name))

    def remove_contact(self):
        row = self.contact_list.currentRow()
        self.contact_list.takeItem(row)

    def remove_all_contacts(self):
        self.contacts.clear()
        self.contact_list.clear()

    def apply(self):
        self.contacts.clear()
        with open("local_storage/temp/contacts.json") as read_file:
            contacts = json.load(read_file)
            for row in range(self.contact_list.count()):
                contact_info = contacts[f"contact{row}"]
                name = contact_info["name"]
                email = contact_info["email"]

                self.contacts.update({name:email})

    def load_contacts(self, api):
        self.contact_list.clear()
        with open("local_storage/temp/api.json") as read_file:
            apis = json.load(read_file)
    
        selected_contacts = apis[f"api{api}"]["recipients"]
        for contact in selected_contacts:
            self.contact_list.addItem(QListWidgetItem(contact))

        with open("local_storage/temp/contacts.json") as read_file:
            contact_table = json.load(read_file)
        
        for contact in range(len(contact_table)):
            self.select_contact_list.addItem(QListWidgetItem(contact_table[f"contact{contact}"]["name"]))
            
    def set_default(self):
        self.contacts.clear()
        self.contact_list.clear()

    def reload(self):
        self.select_contact_list.clear()
        try:
            with open("local_storage/temp/contacts.json") as open_file:
                contacts = json.load(open_file)
            
            self.select_contact_list.clear()
            for contact in range(len(contacts)):
                self.select_contact_list.addItem(contacts[f"contact{contact}"]["name"])

        except (AttributeError, json.decoder.JSONDecodeError):
            print("Error reloading contacts")


            