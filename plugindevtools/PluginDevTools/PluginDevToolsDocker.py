from krita import *
from .PluginDevToolsWidget import *


DOCKER_TITLE = 'Plugin Developer Tools'

class PluginDevToolsDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.mainWidget = PluginDevToolsWidget()
        self.setWidget(self.mainWidget)

    def canvasChanged(self, canvas):
        pass
        
