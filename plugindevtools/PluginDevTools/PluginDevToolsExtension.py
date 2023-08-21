from krita import *

## TODO: Planed to add some functions in future.

#class PluginDevToolsExtension(Extension):
#    def __init__(self, parent):
#        super().__init__(parent) 
#
#    # Krita.instance() exists, so do any setup work
#    def setup(self):
#        pass
#
#    # called after setup(self)
#    def createActions(self, window):
#        pass


# This is a test extension
import inspect
class PluginDevToolsTestExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window: Window):
        action = window.createAction('PluginDevTools', 'PluginDevTools', 'tools/scripts/PluginDevTools')
        self.menu = QMenu('PluginDevTools', window.qwindow())
        action.setMenu(self.menu)
        # Add some fixed Action here:
        #action = window.createAction('actionID', 'actionDisplayName', 'tools/scripts/PluginDevTools')
        #self.menu.addAction(action)
        #action.triggered.connect(someConnectObject)


    def dynamicAddEntry(self, *args):
        # Only for debug
        # How to use in console:
        #debugentry = next((w for w in Krita.instance().extensions() if str(type(w)).__contains__('PluginDevToolsTestExtension')), None)
        #print(vars(debugentry))
        # then use debugentry.yourVariable to access yourVariable
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context
        if string is not None:
            string = string[0].strip()
        else:
            return

        args_name = string[string.find('(') + 1:-1].replace(' ', '').split(',')
    
        for name, value in zip(args_name, args):
            setattr(self, name, value)


    def dynamicCreateAction(self, connectObject, window: QObject, id_text: str, displayName: str = str(), addToMenu=False) ->QAction:
        if not isinstance(window, Window):
            print("PluginDevToolsExtension.dynamicCreateAction: {window} is not an instance of Krita.Window type. Empty QAction was returned.")
            return QAction()
        else:
            action = window.createAction(id_text, displayName)
            action.triggered.connect(connectObject)
            if addToMenu:
                self.menu.addAction(action)

            return action


