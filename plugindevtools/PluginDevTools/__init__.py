from krita import *
from .PluginDevToolsExtension import * 
from .PluginDevToolsDocker import * 
from .PluginDevToolsWidget import *
from .PluginDevToolsDialog import *
from .PluginDevToolsStatusManager import *


app = Krita.instance()

## TODO: Planed to add some functions in future.
## Add to extension list
#extension = PluginDevToolsExtension(parent=app) #instantiate your class
#app.addExtension(extension)

testExtension = PluginDevToolsTestExtension(parent=app)
app.addExtension(testExtension)

# Add to docker list
DOCKER_ID = 'pluginDevToolsDocker'
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockBottom, PluginDevToolsDocker)
app.addDockWidgetFactory(dock_widget_factory)

statusManager = PluginDevToolsStatusManager('statusManager')

def retrieveDocker(docker_id: str)->PluginDevToolsDocker:
    # Only retrieve docker instance after the main window was completely created
    try:
        Krita.instance().activeWindow().qwindow()
    except:
        print('main window not created at this moment')
        return PluginDevToolsDocker()

    for d in app.dockers():
        if d.objectName() == docker_id:
            if isinstance(d, PluginDevToolsDocker):
                return d
    print("cannot find docker: {docker_id}")
    exit(1)


def setup():
    global statusManager

    qwin = Krita.instance().activeWindow().qwindow()


    docker = retrieveDocker(DOCKER_ID)
    statusManager.setDocker(docker)
    
    # Prepare a standalone window
    dialog = PluginDevToolsDialog()
    statusManager.setDialog(dialog)
    
    # Prepare content widget. This widget will be added into docker or dialog. Only keep one instance.
    centralwidget = PluginDevToolsWidget()
    statusManager.setCentralWidget(centralwidget)
    
    # Set dialog's parent to qwindow, when close qwindow, dialog will be closed as well
    statusManager.dialog.setParent(qwin)
    # Reset windowflag to keep as a standalone window
    # Should always reset windowflag after setParent
    statusManager.dialog.setWindowFlag(Qt.WindowType.Window, True)

    statusManager.setFirstAfterStart()

    # Status route: modeAllHide <--> modeDocker <--> modeDialog
    statusManager.dialog.signal_closed.connect(lambda : statusManager.applyDockerMode('dialog.signal_closed'))
    statusManager.docker.signal_leaveFloating.connect(lambda : statusManager.applyDialogMode('docker.signal_leaveFloating'))
    statusManager.docker.signal_manualOpenDocker.connect(lambda : statusManager.applyDockerMode('docker.signal_manualOpenDocker'))


    # Only for debug
    testExtension.dynamicAddEntry(DOCKER_ID, dock_widget_factory, centralwidget, dialog, docker, statusManager)

    # Dynamically load some object into actions menu
    testExtension.dynamicCreateAction(statusManager.applyDockerMode, Krita.instance().activeWindow(), 'PluginDevToolsActionOpenAsDocker', 'Open as Docker', True)
    testExtension.dynamicCreateAction(statusManager.applyDialogMode, Krita.instance().activeWindow(), 'PluginDevToolsActionOpenAsDialog', 'Open as Dialog', True)
    def toggleOnAndOff():
        if statusManager.docker.isVisible():
            statusManager.applyHideMode()
        else:
            statusManager.applyDockerMode()
    testExtension.dynamicCreateAction(toggleOnAndOff, Krita.instance().activeWindow(), 'PluginDevToolsToggleOnOff', 'Toggle On or Off')



# Some settings require Krita.instance().activeWindow().qwindow() as parameter
# Wait Krita.instance().activeWindow().qwindow() completely created then set the widgets
appNotifier = Krita.instance().notifier()
appNotifier.setActive(True)
appNotifier.windowCreated.connect(setup)
#appNotifier.applicationClosing.connect(statusManager.saveLastBeforeExit)


