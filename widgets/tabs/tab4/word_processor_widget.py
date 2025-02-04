from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]


class WordProcessor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load all stylesheets sequentially
        stylesheet = ""
        with open("widgets/custom_widget_styles/word_processor.qss", 'r') as f:
            stylesheet += f.read()

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            stylesheet += f.read()

        self.setStyleSheet(stylesheet)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.subject_line = QLineEdit()
        self.subject_line.setObjectName("subject-line")
        self.subject_line.setPlaceholderText("Enter Subject Line: ")
        self.subject_line.setStyleSheet("QLineEdit:focus {background-color: #f4f8ff; border: 1px solid #007bff;}")

        self.editor = QTextEdit()

        self.editor.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)
        font = QFont('Times', 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)
        self.path = None
        self.color = QColor("#000000")
        self.highlight = QColor("#ffffff")

        self.toolbar_frame = QWidget(self)
        self.toolbar_frame.layout = QHBoxLayout()
        self.toolbar_frame.setLayout(self.toolbar_frame.layout)
        self.toolbar_frame.setStyleSheet(
            "QToolButton:!hover {border:2px solid #f0f0f0 ; background-color:white;}"
            "QToolButton:checked {background-color: #c1c1c1}"
            )

        format_toolbar = QToolBar("Format")
        format_toolbar.setObjectName("toolbar")
        format_toolbar.setStyleSheet(
            "QToolBar#toolbar {background-color:lightGray}"
            )
        self.toolbar_frame.layout.addWidget(format_toolbar)

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.setFixedHeight(self.toolbar_frame.height() + 1)
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.setFixedHeight(self.toolbar_frame.height() + 3)
        self.fontsize.addItems([str(s) for s in FONT_SIZES])
        self.fontsize.currentTextChanged.connect(lambda s: self.editor.setFontPointSize(float(s)))
        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(QIcon("assets/word_processor_icons/edit-bold.png"), "B", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.StandardKey.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Weight.Bold if x else QFont.Weight.Normal))
        format_toolbar.addAction(self.bold_action)

        self.italic_action = QAction(QIcon("assets/word_processor_icons/edit-italic.png"), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.StandardKey.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)

        self.underline_action = QAction(QIcon("assets/word_processor_icons/edit-underline.png"), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.StandardKey.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)


        self.alignl_action = QAction(QIcon("assets/word_processor_icons/edit-alignment-left.png"), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft))
        format_toolbar.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon("assets/word_processor_icons/edit-alignment-center.png"), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter))
        format_toolbar.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon("assets/word_processor_icons/edit-alignment-right.png"), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignRight))
        format_toolbar.addAction(self.alignr_action)

        self.alignj_action = QAction(QIcon("assets/word_processor_icons/edit-alignment-justify.png"), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify))
        format_toolbar.addAction(self.alignj_action)

        self.color_action = QToolButton(self)
        self.color_action.setToolTip("Text Color")
        self.color_action.setStatusTip("Text Color")
        self.color_action.setFixedSize(self.toolbar_frame.height()*1.5, self.toolbar_frame.height()+2)
        self.color_action.setText("A")
        self.color_action.setStyleSheet(f"color: {self.color.name()}")
        self.color_action.clicked.connect(self.get_color)
        format_toolbar.addWidget(self.color_action)

        self.highlight_action = QToolButton(self)
        self.highlight_action.setToolTip("Highlight Color")
        self.highlight_action.setStatusTip("Highlight Color")
        self.highlight_action.setFixedSize(self.toolbar_frame.height()*1.5, self.toolbar_frame.height()+2)
        self.highlight_action.setText("A")
        self.highlight_action.setStyleSheet(f"background-color: {self.highlight.name()}")
        self.highlight_action.clicked.connect(self.get_background_color)
        format_toolbar.addWidget(self.highlight_action)

        self.upload_action = QToolButton(self)
        self.upload_action.setToolTip("Upload Media")
        self.upload_action.setStatusTip("Upload Media")
        self.upload_action.setIcon(QIcon("assets/add_media.png"))  # Set the icon
        self.upload_action.setIconSize(QSize(36, 36))  # Set icon size if needed
        self.upload_action.clicked.connect(self.open_file_dialog)
        self.upload_action.setStyleSheet("""
            QToolButton:hover {
                background-color: #ffffff; /* Ensure no change on hover */
            }
        """)

        # Adjust size policy if necessary
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.upload_action.setSizePolicy(size_policy)

        format_toolbar.addWidget(self.upload_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)


        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            self.color_action,
            self.highlight_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        layout.addWidget(self.toolbar_frame)
        layout.addWidget(self.subject_line)
        layout.addWidget(self.editor)

        self.update_format()
    
    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp *.gif)", 
                                    "Videos (*.mp4 *.avi *.mov *.mkv)", 
                                    "All Files (*)"])
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # Handle the selected file(s) as needed
                file_path = selected_files[0]
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_format = QTextImageFormat()
                    image_format.setName(file_path)
                    image = QImage(file_path)
                    if not image.isNull():
                        image_format.setWidth(image.width())
                        image_format.setHeight(image.height())
                        cursor = self.editor.textCursor()
                        cursor.insertImage(image_format)
                else:
                    print(f"Uploaded media file: {file_path}")

    def get_color(self):
        self.editor.setTextColor(QColorDialog.getColor())
        self.color_action.setStyleSheet(f"color: {self.editor.textColor().name()}")

    def get_background_color(self):
        new_color = QColorDialog.getColor(initial=self.editor.textBackgroundColor())
        if new_color.isValid():
            self.editor.setTextBackgroundColor(new_color)
            self.highlight_action.setStyleSheet(f"background-color: {new_color.name()};")


    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is necessary to keep
        toolbars/etc. in sync with the current edit state.
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Weight.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignJustify)

        self.color_action.setStyleSheet(f"color: {self.editor.textColor().name()}")
        self.highlight_action.setStyleSheet(f"background-color: {self.editor.textBackgroundColor().name()}")

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html)")

        try:
            with open(path, 'r') as f:
                text = f.read()

        except FileNotFoundError:
            pass

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html
            self.editor.setText(text)

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toHtml()

        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = self.editor.toHtml()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
        
    def setPlaceholderText(self, text):
        self.editor.setPlaceholderText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordProcessor()
    window.show()
    sys.exit(app.exec())
