from PySide6 import QtCore, QtGui, QtWidgets


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        hint = super().tabSizeHint(index).transposed()
        return QtCore.QSize(
            max(hint.width(), 200), 
            max(hint.height(), 70)
        )

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        current = self.currentIndex()
        for i in range(self.count()):
            if i == current:
                continue
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, opt)
            opt.shape = QtWidgets.QTabBar.Shape.RoundedNorth
            painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, opt)

        self.initStyleOption(opt, current)
        painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, opt)
        opt.shape = QtWidgets.QTabBar.Shape.RoundedNorth
        painter.drawControl(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, opt)

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        tab_bar = TabBar(self)
        font = tab_bar.font()
        font.setPointSize(20)
        font.setBold(True)
        tab_bar.setFont(font)

        self.setTabBar(tab_bar)
        self.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)

        with open("widgets/custom_widget_styles/widgetsGeneralStyles.qss", 'r') as f:
            self.setStyleSheet(f.read())

    def resizeEvent(self, event):
            self.tabBar().setFixedHeight(self.height())
            super(TabWidget, self).resizeEvent(event)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = TabWidget()
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom.png"), "ABC   ")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom-in.png"), "ABCDEFGH")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom-out.png"), "XYZ")

    w.resize(640, 480)
    w.show()

    sys.exit(app.exec())