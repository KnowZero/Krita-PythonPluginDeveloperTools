from krita import *
from .PluginDevToolsWidget import *


DOCKER_TITLE = 'Plugin Developer Tools'


class PluginDevToolsDialog(QMainWindow):
    signal_closed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.setWindowTitle(DOCKER_TITLE)

    def updateWindowTitle(self):
        if isinstance(self.parentWidget(), QWidget):
            self.setObjectName("PluginDevToolsDialog_" + self.parentWidget().objectName())
            if self.parentWidget().windowTitle().__len__() == 0:
                self.setWindowTitle(DOCKER_TITLE)
            else:
                self.setWindowTitle(self.parentWidget().windowTitle() + ' - ' + DOCKER_TITLE)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.signal_closed.emit()
        return super().closeEvent(event)



class PluginDevToolsDocker(DockWidget):
    signal_leaveFloating = pyqtSignal()
    signal_manualOpenDocker = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.titleBarEventListening = False
        self.installEventFilter(self)
        # Prepare a standalone window
        self.floatModeDialog = PluginDevToolsDialog(self.parent())
        # Prepare content widget. This widget will be added into docker itself or self.floatModeDialog. Only keep one instance.
        self.centralWidget = PluginDevToolsWidget()
        self.mutex = QMutex()
        # Status route: modeAllHide <--> modeDocker <--> modeDialog
        self.floatModeDialog.signal_closed.connect(lambda : self.applyDockerMode('dialog.signal_closed'))
        self.signal_leaveFloating.connect(lambda : self.applyDialogMode('docker.signal_leaveFloating'))
        self.signal_manualOpenDocker.connect(lambda : self.applyDockerMode('docker.signal_manualOpenDocker'))

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

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QEvent.Type.ParentChange:
            if isinstance(self.parentWidget(), QWidget):
                self.floatModeDialog.setParent(self.parentWidget())
                # Always reset window type after manually setParent
                self.floatModeDialog.setWindowFlag(Qt.WindowType.Window)
                self.parentWidget().windowTitleChanged.connect(self.floatModeDialog.updateWindowTitle)

        return super().changeEvent(event)


    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.titleBarWidget():
            if event.type() == QEvent.Type.MouseButtonDblClick:
                if not self.isFloating():
                    self.signal_leaveFloating.emit()
                    return True

        return super().eventFilter(obj, event)


    def setFirstAfterStart(self):
        # Initialize the first status after start Krita
        if self.isFloating():
            self.applyDialogMode('initiallize')
        elif self.isVisible():
            self.applyDockerMode('initiallize')
        else:
            self.applyHideMode('initiallize')


    def applyHideMode(self, senderName=str()):
        if self.mutex.tryLock() == False:
            #print('skipped applyHideMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.setFloating(False)
        self.setWidget(self.centralWidget)
        self.close()
        self.floatModeDialog.close()
        self.mutex.unlock()


    def applyDockerMode(self, senderName=str()):
        if self.mutex.tryLock() == False:
            #print('skipped applyDockerMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.setFloating(False)
        self.setWidget(self.centralWidget)
        self.show()
        self.floatModeDialog.close()
        self.mutex.unlock()


    def applyDialogMode(self, senderName=str()):
        if self.mutex.tryLock() == False:
            #print('skipped applyDialogMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.setFloating(False)
        self.close()
        self.floatModeDialog.setCentralWidget(self.centralWidget)
        self.floatModeDialog.show()
        self.floatModeDialog.activateWindow()
        newWidth = self.floatModeDialog.size().width()
        newPoint = QCursor.pos()
        newPoint.setX(newPoint.x()-int(newWidth/2))
        self.floatModeDialog.move(self.floatModeDialog.mapFrom(self.floatModeDialog, newPoint))
        self.mutex.unlock()


