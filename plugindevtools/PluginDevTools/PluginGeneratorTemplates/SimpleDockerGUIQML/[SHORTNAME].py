try:
    from PyQt6.QtWidgets import *
except:
    from PyQt5.QtWidgets import *
'''[%AUTOCOMPLETE%]'''
try:
    from PyQt6 import uic
except:
    from PyQt5 import uic

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
