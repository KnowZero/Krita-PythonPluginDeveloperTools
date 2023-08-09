from krita import *
from .PluginDevToolsExtension import * 
from .PluginDevToolsDocker import * 


app = Krita.instance()

# Add to extension list
extension = PluginDevToolsExtension(parent=app) #instantiate your class
app.addExtension(extension)

# Add to docker list
DOCKER_ID = 'pluginDevToolsDocker'
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockBottom, PluginDevToolsDocker)
app.addDockWidgetFactory(dock_widget_factory)
