from krita import *
from PyQt5.QtWidgets import QMainWindow
from .PluginDevToolsWidget import *

class PluginDevToolsDialog(QMainWindow):
    signal_closed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.setWindowTitle('Plugin Developer Tools')


    def closeEvent(self, event: QtGui.QCloseEvent):
        self.signal_closed.emit()
        return super().closeEvent(event)


