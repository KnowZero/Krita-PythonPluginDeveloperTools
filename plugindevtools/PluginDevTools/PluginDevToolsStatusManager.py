from krita import *
from PyQt5.QtCore import *
from .PluginDevToolsWidget import *
from .PluginDevToolsDocker import *
from .PluginDevToolsDialog import *


class PluginDevToolsStatusManager():
    # shared with all instances
    mutex = QMutex()

    def __init__(self, name=str()):
        self.__objectname = name
        self.docker: PluginDevToolsDocker
        self.dialog: PluginDevToolsDialog
        self.centralwidget: PluginDevToolsWidget


    def objectName(self):
        # Only for debug
        return self.__objectname


    def setDocker(self, docker: PluginDevToolsDocker):
        self.docker = docker


    def setDialog(self, dialog: PluginDevToolsDialog):
        self.dialog = dialog


    def setCentralWidget(self, centralwidget: PluginDevToolsWidget):
        self.centralwidget = centralwidget


    def setFirstAfterStart(self):
        # Initialize the first status after start Krita
        if self.docker.isFloating():
            self.applyDialogMode('initiallize')
        elif self.docker.isVisible():
            self.applyDockerMode('initiallize')
        else:
            self.applyHideMode('initiallize')


    def applyHideMode(self, senderName=str()):
        if type(self).mutex.tryLock() == False:
            #print('skipped applyHideMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.docker.setFloating(False)
        self.docker.setWidget(self.centralwidget)
        self.docker.close()
        self.dialog.close()
        type(self).mutex.unlock()


    def applyDockerMode(self, senderName=str()):
        if type(self).mutex.tryLock() == False:
            #print('skipped applyDockerMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.docker.setFloating(False)
        self.docker.setWidget(self.centralwidget)
        self.docker.show()
        self.dialog.close()
        type(self).mutex.unlock()


    def applyDialogMode(self, senderName=str()):
        if type(self).mutex.tryLock() == False:
            #print('skipped applyDialogMode')
            #print('    mutex.tryLock()= ', False)
            #print('    sender= ', senderName)
            #print('')
            return
        self.docker.setFloating(False)
        self.docker.close()
        self.dialog.layout().addWidget(self.centralwidget)
        self.dialog.show()
        self.dialog.activateWindow()
        type(self).mutex.unlock()


