import krita

if int(krita.Krita.instance().version().split('.')[0]) >= 6:
    from PyQt6.QtWidgets import *
else:
    from PyQt5.QtWidgets import *
'''[%AUTOCOMPLETE%]'''

class '''[%SHORTNAME%]'''(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")
        label = QLabel(self)
        label.setObjectName("label")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText("Hello World")
        
        self.centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.centralWidget.setLayout(layout)
        
        self.setWidget(self.centralWidget)
       


    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("'''[%SHORTNAME%]'''", DockWidgetFactoryBase.DockPosition.DockRight, '''[%SHORTNAME%]''')) 
