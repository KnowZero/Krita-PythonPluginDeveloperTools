from krita import *
from PyQt5.QtWidgets import QDialog, QHBoxLayout
from .PluginDevToolsWidget import *

class PluginDevToolsDialog(QDialog):
    signal_closed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)
        self.setWindowTitle('Plugin Developer Tools')
        # Can keep a standalone window after setParent with qwin
        self.setWindowFlag(Qt.WindowType.Window, True)


    def closeEvent(self, event: QtGui.QCloseEvent):
        self.signal_closed.emit()
        return super().closeEvent(event)


