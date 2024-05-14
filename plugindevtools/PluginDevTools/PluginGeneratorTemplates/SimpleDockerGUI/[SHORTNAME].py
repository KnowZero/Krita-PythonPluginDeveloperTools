from PyQt5.QtWidgets import *
'''[%AUTOCOMPLETE%]'''

class '''[%SHORTNAME%]'''(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")
        label = QLabel(self)
        label.setObjectName("label")
        label.setAlignment(Qt.AlignCenter)
        label.setText("Hello World")
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        self.layout().addItem(layout)
       


    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("'''[%SHORTNAME%]'''", DockWidgetFactoryBase.DockRight, '''[%SHORTNAME%]''')) 
