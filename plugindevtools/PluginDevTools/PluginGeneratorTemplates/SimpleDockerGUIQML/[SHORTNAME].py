from PyQt5.QtWidgets import *
'''[%AUTOCOMPLETE%]'''
from PyQt5 import uic

class '''[%SHORTNAME%]'''(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")
        self.centralWidget = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),"'''[%SHORTNAME%]'''.ui"))
        
        self.setWidget(self.centralWidget)

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("'''[%SHORTNAME%]'''", DockWidgetFactoryBase.DockRight, '''[%SHORTNAME%]''')) 
