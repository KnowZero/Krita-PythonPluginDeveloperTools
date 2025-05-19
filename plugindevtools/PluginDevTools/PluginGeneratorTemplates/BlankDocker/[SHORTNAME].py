import krita
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6.QtWidgets import *
except:
    from PyQt5.QtWidgets import *
'''[%AUTOCOMPLETE%]'''

class '''[%SHORTNAME%]'''(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("'''[%SHORTNAME%]'''", DockWidgetFactoryBase.DockPosition.DockRight, '''[%SHORTNAME%]''')) 
