from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        
        self.intro_graphic_pxm = QtGui.QPixmap("assets/intro_graphic.png")
        self.intro_graphic_lb = QLabel(self)
        self.intro_graphic_lb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.intro_graphic_lb.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.intro_graphic_lb, 0, 0)
        self.update_image_size()

    def resizeEvent(self, event):
        self.update_image_size()
        super().resizeEvent(event)

    def update_image_size(self):
        """ Resize the image dynamically while keeping the aspect ratio. """
        if not self.intro_graphic_pxm.isNull():
            scaled_pixmap = self.intro_graphic_pxm.scaled(
                self.size() * 0.8,  # Scale to 80% of the available size
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            self.intro_graphic_lb.setPixmap(scaled_pixmap)
