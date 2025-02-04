
from PySide6.QtWidgets import QPushButton, QMessageBox, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QScrollArea, QWidget, QDialog, QFormLayout, QLineEdit, QComboBox, QSizePolicy, QLayout, QWidgetItem
from PySide6.QtGui import QFont, QIcon
from PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QRect, QPoint

class AddCropCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("addCropCard")
        self.setStyleSheet("""
            #addCropCard {
                background-color: rgb(45, 75, 65);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                min-height: 200px;
                max-height: 200px;
                min-width: 250px;
                max-width: 250px;
                margin: 10px;
            }
            #addCropCard:hover {
                background-color: rgb(55, 85, 75);
                border-color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Plus icon
        plus_label = QLabel("+")
        plus_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        layout.addWidget(plus_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Add New Crop text
        add_label = QLabel("Add New Crop")
        add_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 18px;
            font-weight: medium;
        """)
        layout.addWidget(add_label, alignment=Qt.AlignmentFlag.AlignHCenter)

class CropCard(QFrame):
    def __init__(self, crop_data=None, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.crop_data = crop_data
        self.setObjectName("cropCard")
        self.setStyleSheet("""
            #cropCard {
                background-color: rgb(45, 75, 65);
                border-radius: 12px;
                min-height: 200px;
                max-height: 200px;
                min-width: 250px;
                max-width: 250px;
                margin: 10px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                padding: 4px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QLabel {
                color: white;
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Top row with title and action buttons
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        # Crop name (title)
        name_label = QLabel(crop_data["name"])
        name_label.setObjectName("name_label")  # Set object name for easy access
        name_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        top_row.addWidget(name_label)
        
        # Spacer to push buttons to the right
        top_row.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        
        edit_btn.setFixedSize(60, 30)
        delete_btn.setFixedSize(60, 30)
        
        edit_btn.clicked.connect(self.edit_card)
        delete_btn.clicked.connect(self.delete_card)
        
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        top_row.addLayout(button_layout)
        
        layout.addLayout(top_row)
        
        # Add a separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        layout.addWidget(line)
        
        # Crop details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)
        
        for key, value in [
            ("Variety", crop_data["variety"]),
            ("Type", crop_data["type"]),
        ]:
            info_layout = QHBoxLayout()
            key_label = QLabel(f"{key}:")
            key_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
            """)
            value_label = QLabel(value)
            value_label.setObjectName(f"{key.lower()}_label")  # Set object name for easy access
            value_label.setStyleSheet("""
                color: white;
                font-size: 14px;
                font-weight: medium;
            """)
            
            info_layout.addWidget(key_label)
            info_layout.addWidget(value_label)
            info_layout.addStretch()
            details_layout.addLayout(info_layout)
        
        layout.addLayout(details_layout)
        layout.addStretch()

    def edit_card(self):
        if self.parent:
            self.parent.edit_crop(self)

    def delete_card(self):
        if self.parent:
            self.parent.delete_crop(self)

class ContactsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header Label
        header_layout = QHBoxLayout()
        self.table_info_lb = QLabel("Add and Edit Crops")
        self.table_info_lb.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(self.table_info_lb)
        header_layout.addStretch()
        
        # Error Label
        self.error_lb = QLabel(self)
        self.error_lb.setStyleSheet("color: red; font-size: 14px;")
        header_layout.addWidget(self.error_lb)
        
        self.layout.addLayout(header_layout)
        
        # Add Crop Dialog
        self.setup_add_crop_dialog()
        
        # Scroll Area for Cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        # Container for cards
        self.cards_container = QWidget()
        self.cards_layout = QFlowLayout()
        self.cards_layout.setSpacing(5)  # Reduced spacing between cards
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_container.setLayout(self.cards_layout)
        
        scroll.setWidget(self.cards_container)
        self.layout.addWidget(scroll)
        
        # Reset edit mode flag
        self.is_edit_mode = False
        self.card_being_edited = None

        # Add the "Add New" card
        self.add_new_card = AddCropCard(self)
        self.add_new_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_new_card.mousePressEvent = lambda e: self.show_add_dialog()
        self.cards_layout.addWidget(self.add_new_card)    # Add these methods to handle edit and delete operations

    def edit_crop(self, card):
        # Reset dialog to clear previous state
        self.reset_add_dialog()
        
        self.is_edit_mode = True
        self.card_being_edited = card
        
        # Populate dialog with existing crop data
        self.add_crop_name_tb.setText(card.crop_data["name"])
        self.variety_dropdown.setCurrentText(card.crop_data["variety"])
        self.type_dropdown.setCurrentText(card.crop_data["type"])
        
        # Change save button to update
        self.save_btn.setText("Update")
        self.save_btn.clicked.disconnect()
        self.save_btn.clicked.connect(self.update_crop)
        
        self.add_dialog.exec()

    def update_crop(self):
        name = self.add_crop_name_tb.text()
        if not name:
            self.error_lb.setText("Please enter crop name.")
            return
        
        # Update the crop data
        if self.card_being_edited:
            self.card_being_edited.crop_data.update({
                "name": name,
                "variety": self.variety_dropdown.currentText(),
                "type": self.type_dropdown.currentText(),
            })
            
            # Update the labels directly
            self.card_being_edited.findChild(QLabel, "name_label").setText(name)
            self.card_being_edited.findChild(QLabel, "variety_label").setText(self.variety_dropdown.currentText())
            self.card_being_edited.findChild(QLabel, "type_label").setText(self.type_dropdown.currentText())
        
        # Reset dialog and related state
        self.reset_add_dialog()
        self.add_dialog.accept()
    
    def reset_add_dialog(self):
        # Reset all dialog elements to default state
        self.add_crop_name_tb.clear()
        self.variety_dropdown.setCurrentIndex(0)
        self.type_dropdown.setCurrentIndex(0)
        
        # Reset save button to default
        self.save_btn.setText("Save")
        self.save_btn.clicked.disconnect()
        self.save_btn.clicked.connect(self.add_new_crop)
        
        # Reset edit mode
        self.is_edit_mode = False
        self.card_being_edited = None
        self.error_lb.clear()

    def delete_crop(self, card):
        # Show confirmation dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirm Delete")
        confirm.setText(f"Are you sure you want to delete {card.crop_data['name']}?")
        confirm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm.setIcon(QMessageBox.Icon.Question)
        
        if confirm.exec() == QMessageBox.StandardButton.Yes:
            try:
                # Get the index of the card in the layout
                index = self.cards_layout.indexOf(card)
                if index != -1:
                    # Remove the card from the layout and delete it
                    self.cards_layout.takeAt(index)
                    card.deleteLater()
                    
                    # Update layout and refresh UI
                    self.cards_container.updateGeometry()  # Force re-layout
                    self.cards_container.adjustSize()     # Adjust container size if needed

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")


    def setup_add_crop_dialog(self):
        self.add_dialog = QDialog(self)
        self.add_dialog.setWindowTitle("Add New Crop")
        self.add_dialog.setStyleSheet("""
            QDialog {
                background-color: rgb(45, 75, 65);
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                padding: 5px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background-color: rgb(60, 90, 80);
                color: white;
            }
            QComboBox {
                padding: 5px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background-color: rgb(60, 90, 80);
                color: white;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: rgb(70, 120, 110);
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgb(80, 130, 120);
            }
        """)
        
        dialog_layout = QVBoxLayout(self.add_dialog)
        dialog_layout.setSpacing(15)
        dialog_layout.setContentsMargins(20, 20, 20, 20)
        
        # Form Layout
        form = QFormLayout()
        form.setSpacing(10)
        
        self.add_crop_name_tb = QLineEdit()
        self.add_crop_name_tb.setPlaceholderText("Enter crop name")
        self.variety_dropdown = QComboBox()
        self.variety_dropdown.addItems(["Hybrid", "Non-Hybrid"])
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Annual", "Perennial"])

        
        form.addRow("Crop Name:", self.add_crop_name_tb)
        form.addRow("Variety:", self.variety_dropdown)
        form.addRow("Type:", self.type_dropdown)
        
        dialog_layout.addLayout(form)
        
        # Buttons
        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        self.save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        # Direct connection to the add_new_crop method
        self.save_btn.clicked.connect(self.add_new_crop)
        cancel_btn.clicked.connect(self.add_dialog.reject)
        
        buttons.addWidget(self.save_btn)
        buttons.addWidget(cancel_btn)
        dialog_layout.addLayout(buttons)
        
        # Set fixed size for dialog
        self.add_dialog.setFixedSize(350, 250)

    def show_add_dialog(self):
        # Ensure dialog is in add mode
        self.reset_add_dialog()
        self.add_dialog.exec()

    def add_new_crop(self):
        name = self.add_crop_name_tb.text()
        if not name:
            self.error_lb.setText("Please enter crop name.")
            return
            
        crop_data = {
            "name": name,
            "variety": self.variety_dropdown.currentText(),
            "type": self.type_dropdown.currentText(),
        }
        
        try:
            # Remove the "Add New" card temporarily
            add_new_card_item = self.cards_layout.takeAt(self.cards_layout.count() - 1)
            
            # Create and add new crop card
            new_card = CropCard(crop_data, self)
            self.cards_layout.addWidget(new_card)
            
            # Add back the "Add New" card
            if add_new_card_item:
                self.cards_layout.addItem(add_new_card_item)
            
            # Reset dialog
            self.reset_add_dialog()
            self.add_dialog.accept()
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            import traceback
            print(traceback.format_exc())
    
    def save_contacts_dict(self):
        contacts = {}
        for i in range(self.cards_layout.count() - 1):  # -1 to exclude add new card
            item = self.cards_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if isinstance(card, CropCard):
                    contact = {
                        "name": card.crop_data["name"],
                        "variety": card.crop_data["variety"],
                        "type": card.crop_data["type"],
                    }
                    contacts[f"contact{i}"] = contact
        return contacts

class QFlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()