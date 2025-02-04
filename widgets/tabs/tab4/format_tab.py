from PySide6.QtWidgets import *
from PySide6 import QtGui
from widgets.tabs.tab4 import (draft_window, format_help_window, word_processor_widget, ai_writer_window)
from unidecode import unidecode
import re

class FormatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        with open("widgets/custom_widget_styles/word_processor.qss", 'r') as f:
            self.setStyleSheet(f.read())

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())

        self.format_editor = word_processor_widget.WordProcessor(self)
        self.format_editor.setPlaceholderText("Compose the final draft of your email here.")
        self.layout.addWidget(self.format_editor, 1, 0, 1, 4)

        self.subject_tb = self.format_editor.subject_line

        self.get_info_btn = QPushButton("Get Variable Data", self)
        self.layout.addWidget(self.get_info_btn, 2, 0)

        self.show_draft_btn = QPushButton("Show Draft", self)
        self.draft_window = draft_window.DraftWindow()
        self.layout.addWidget(self.show_draft_btn, 2, 1)

        self.show_help_btn = QPushButton(QtGui.QIcon("assets/help_icon.png"), "Help", self)
        self.help_window = format_help_window.FormatHelpWindow()
        self.show_help_btn.clicked.connect(self.help_window.show)
        self.layout.addWidget(self.show_help_btn, 2, 2)

        self.ai_writer_btn = QPushButton(QtGui.QIcon("assets/ai_icon.png"), "Generate Email", self)
        self.ai_writer_btn.setStyleSheet("QPushButton {background-color: #7f43ab} QPushButton:hover{background-color: #de5fc9}")
        
        self.ai_writer_window = ai_writer_window.AIWriterWindow()
        self.ai_writer_window.accept_btn.clicked.connect(self.accept_ai)
        self.ai_writer_btn.clicked.connect(self.ai_writer_window.show)
        self.layout.addWidget(self.ai_writer_btn, 2, 3)

    def accept_ai(self):
        generated_text = self.ai_writer_window.draft_text.toHtml()
        self.ai_writer_window.close()
        self.format_editor.editor.setHtml(generated_text)

    def clear_all(self):
        self.format_editor.editor.clear()
        self.format_editor.subject_line.clear()

    def export_format_html(self, payload: dict):
        new_text = self.format_editor.editor.toHtml()

        for api in range(len(payload)):
            for data in payload[f"api{api}"]:

                key = str(f"{{{list(data.keys())[0]}}}")
                value = str(list(data.values())[0])

                if re.search(key, new_text) is not None:
                    new_text = re.sub(key, value, new_text)

        self.draft_window.draft_text.setHtml(new_text)
        with open("local_storage/temp/format.html", "w") as write_file:
            write_file.write(unidecode(new_text))
        
    def import_format_html(self):
        with open("local_storage/temp/format.html", "r") as read_file:
            contents = read_file.read()
            self.format_editor.editor.setHtml(contents)

    def save_format_dict(self):
        format_dict = {
            "subject" : self.subject_tb.text(),
            "body" : self.format_editor.editor.toHtml()
        }
        return format_dict