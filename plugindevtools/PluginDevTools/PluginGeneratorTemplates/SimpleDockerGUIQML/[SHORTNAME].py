import krita
import os
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6 import uic
    from PyQt6.QtWidgets import *
except:
    from PyQt5 import uic
    from PyQt5.QtWidgets import *

'''[%AUTOCOMPLETE%]'''

class '''[%SHORTNAME%]'''(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")
        self.centralWidget = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),"'''[%SHORTNAME%]'''.ui"))
        
        layout = QVBoxLayout()
        layout.addWidget(self.centralWidget)
        
        self.setLayout(layout)

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("'''[%SHORTNAME%]'''", DockWidgetFactoryBase.DockPosition.DockRight, '''[%SHORTNAME%]''')) 
