from krita import *
from .PluginDevToolsWidget import *


DOCKER_TITLE = 'Plugin Developer Tools'

class PluginDevToolsDocker(DockWidget):
    signal_leaveFloating = pyqtSignal()
    signal_manualOpenDocker = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.titleBarEventListening = False

    def canvasChanged(self, canvas):
        pass
        
    def showEvent(self, event: QtGui.QShowEvent) -> None:
        #print('PluginDevToolsDocker showEvent')
        #print('    sender= ', self.sender())
        if self.titleBarEventListening == False:
            if isinstance(self.titleBarWidget(), QWidget):
                self.titleBarWidget().installEventFilter(self)

        if isinstance(self.sender(), QAction):
            self.signal_manualOpenDocker.emit()
            return super().showEvent(event)
        # Failed to catch mousePressEvent/mouseReleaseEvent when moving docker
        # Failed to catch clicked/toggled/pressed/released signal when click the docker float button 
        # Use showEvent instead
        if (QGuiApplication.mouseButtons() & Qt.MouseButton.LeftButton):
            # Do not switch immediately when dragging the docker to move
            return super().showEvent(event)

        # LeftButton is released and the docker is not docked
        if self.isFloating():
            self.signal_leaveFloating.emit()
        return super().showEvent(event)


    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.titleBarWidget():
            if event.type() == QEvent.Type.MouseButtonDblClick:
                if not self.isFloating():
                    self.signal_leaveFloating.emit()
                    return True
        return super().eventFilter(obj, event)

