 
from krita import *
from .PluginDevToolsDocker import *

class PluginDevTools(Extension):
    def __init__(self, parent):
        super().__init__(parent) 


    def setup(self):
        pass

    def createActions(self, window):
       action2 = window.createAction("pluginDevTools", "Krita Plugin Developer Tools", "tools/scripts")

# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = PluginDevTools(parent=app) #instantiate your class
app.addExtension(extension)
