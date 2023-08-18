from krita import *
from .PluginDevToolsWidget import *
from .PluginDevToolsDocker import * 
from .PluginDevToolsExtension import *


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

    qwin = Krita.instance().activeWindow().qwindow()

    docker = retrieveDocker(DOCKER_ID)
    
    docker.setFirstAfterStart()

    # Only for debug
    testExtension.dynamicAddEntry(DOCKER_ID, dock_widget_factory, docker)

    # Dynamically load some object into actions menu
    testExtension.dynamicCreateAction(docker.applyDockerMode, Krita.instance().activeWindow(), 'PluginDevToolsActionOpenAsDocker', 'Open as Docker', True)
    testExtension.dynamicCreateAction(docker.applyDialogMode, Krita.instance().activeWindow(), 'PluginDevToolsActionOpenAsDialog', 'Open as Dialog', True)
    def toggleOnAndOff():
        if docker.isVisible():
            docker.applyHideMode()
        else:
            docker.applyDockerMode()
    testExtension.dynamicCreateAction(toggleOnAndOff, Krita.instance().activeWindow(), 'PluginDevToolsToggleOnOff', 'Toggle On or Off')



# Some settings require Krita.instance().activeWindow().qwindow() as parameter
# Wait Krita.instance().activeWindow().qwindow() completely created then set the widgets
appNotifier = Krita.instance().notifier()
appNotifier.setActive(True)
appNotifier.windowCreated.connect(setup)


