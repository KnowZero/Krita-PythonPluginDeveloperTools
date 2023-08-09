from krita import *
from PyQt5.QtWidgets import QDialog, QHBoxLayout
from .PluginDevToolsWidget import *

class PluginDevToolsExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent) 


    def setup(self):
        pass

    def initialize(self):
        self.dialog = QDialog()

        self.dialogLayout = QHBoxLayout()
        self.dialog.setLayout(self.dialogLayout)

        self.dialogLayoutContent = PluginDevToolsWidget()
        self.dialogLayout.addWidget(self.dialogLayoutContent)

        self.dialog.setWindowTitle('Plugin Developer Tools')
        self.dialog.show()

    def createActions(self, window):
        action = window.createAction("pluginDevTools", "Plugin Developer Tools", "tools/scripts")
        action.triggered.connect(self.initialize)


