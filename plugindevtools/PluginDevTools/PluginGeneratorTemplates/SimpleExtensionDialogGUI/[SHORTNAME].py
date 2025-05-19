import krita
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6 import uic
    from PyQt6.QtWidgets import *
except:
    from PyQt5 import uic
    from PyQt5.QtWidgets import *

'''[%AUTOCOMPLETE%]'''

class '''[%SHORTNAME%]'''Dialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("'''[%PLUGINTITLE%]'''")
        label = QLabel(self)
        label.setObjectName("label")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText("Hello World")
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        self.setLayout(layout)

class '''[%SHORTNAME%]'''(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.dialog = '''[%SHORTNAME%]'''Dialog()

    def setup(self):
        #This runs only once when app is installed
        pass

    def createActions(self, window):
        action = window.createAction("'''[%SHORTNAME%]'''OpenDialog", "Open '''[%SHORTNAME%]''' Dialog", "tools/scripts")
        action.triggered.connect(self.dialog.show)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension('''[%SHORTNAME%]'''(Krita.instance())) 
