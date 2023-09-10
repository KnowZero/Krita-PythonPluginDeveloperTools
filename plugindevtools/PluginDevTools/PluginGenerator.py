from krita import *
from PyQt5 import uic
import re
import os
import subprocess
import json

from .GetKritaAPI import *

class ActionGeneratorDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        

        self.data = {}
        self.centralWidget = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),'ActionGeneratorWidget.ui') )
        layout = QVBoxLayout()
        layout.addWidget(self.centralWidget)
        
        self.model = QStandardItemModel()
        self.centralWidget.listView.setModel(self.model)

        self.setLayout(layout)
        
        self.centralWidget.newBtn.clicked.connect(self.newItem)
        self.centralWidget.deleteBtn.clicked.connect(self.deleteItem)
        self.centralWidget.saveBtn.clicked.connect(self.saveItem)
        
        self.centralWidget.doneBtn.clicked.connect(self.doneClicked)
        
        self.centralWidget.listView.selectionModel().selectionChanged.connect(self.openItem)
        

    
    def doneClicked(self):
        data={}
        for row in range(0,self.model.rowCount()):
            index = self.model.index(row,0)
            rec=index.data(Qt.UserRole+1)
            if rec['category'] not in data:
                data[rec['category']]={ 'text':rec['categoryText'], 'actions':[]  }
            newRec={}    
            for k in rec.keys():
                newRec[ k.replace('action.','') ]=rec[k]
            data[rec['category']]['actions'].append(newRec)
        self.data = data

        self.close()


    
    def newItem(self, name=None, data=None):
        if not name:
            name='new'
        if not data:
            data=self.defaultForm
        item = QStandardItem(name)
        item.setData(data, Qt.UserRole+1)
        self.model.appendRow(item)
        index = self.model.indexFromItem(item)
        self.centralWidget.listView.selectionModel().select(index, QtCore.QItemSelectionModel.ClearAndSelect)
    def deleteItem(self):
        items = self.centralWidget.listView.selectionModel().selectedIndexes()
        for item in items:
            self.model.removeRow(item.row(),item.parent())
    def openItem(self, old, new):
        items = self.centralWidget.listView.selectionModel().selectedIndexes()
        for item in items:
            data = item.data(Qt.UserRole+1)
            print ("open form", data )
            if data:
                self.loadForm(self.centralWidget, data)
    def saveItem(self):
        items = self.centralWidget.listView.selectionModel().selectedIndexes()
        for item in items:
            data={}
            self.saveForm(self.centralWidget, data)
            print ("SAVE", data, item)
            
            self.model.setData(item,data, Qt.UserRole+1)
            self.model.setData(item,data['action.name'], Qt.DisplayRole)
            self.defaultForm['category']=data['category']
            self.defaultForm['categoryText']=data['categoryText']

    def loadForm(self, form, items):
        for w in form.findChildren(QWidget):
            if '_' not in w.objectName() and hasattr(w,'statusTip') and w.statusTip() != '':
                name = w.statusTip()
                if name in items:
                    v = items[name]
                    if isinstance(w,QLineEdit):
                        w.setText(v)
                    elif isinstance(w,QSpinBox):
                        w.setValue(v)
                    elif isinstance(w,QCheckBox):
                        w.setChecked(v == 'true')
                    elif isinstance(w,QKeySequenceEdit):
                        w.setKeySequence(QKeySequence.fromString(v))
                    elif isinstance(w,QComboBox):
                        if w.currentData():
                            w.setCurrentIndex(w.findData(v))
                        else:
                            w.setCurrentIndex(w.findText(v))
                    elif isinstance(w,QListView) and w.model():
                        index = w.model().match(w.model().index(0, 0),
                                                    Qt.DisplayRole, 
                                                    v,
                                                    1);
                        items[name]=w.setCurrentIndex(index)

    def saveForm(self, form, items):
        for w in form.findChildren(QWidget):
            if '_' not in w.objectName() and hasattr(w,'statusTip') and w.statusTip() != '':
                name = w.statusTip()
                if isinstance(w,QLineEdit):
                    items[name]=w.text()
                elif isinstance(w,QSpinBox):
                    items[name]=w.value()
                elif isinstance(w,QCheckBox):
                    items[name]='true' if w.isChecked() else 'false'
                elif isinstance(w,QKeySequenceEdit):
                    items[name]=w.keySequence().toString()
                elif isinstance(w,QComboBox):
                    if w.currentData():
                        items[name]=w.currentData()
                    else:
                        items[name]=w.currentText()
                elif isinstance(w,QListView) and w.model():
                    items[name]=w.currentIndex().data(Qt.DisplayRole)

        
    def getData(self, data):
        self.defaultForm = {}
        self.saveForm(self.centralWidget,self.defaultForm)
        if data:
            for cat in data.keys():
                for action in range(0,len(data[cat]['actions'])):
                    rec={
                        'category':cat,
                        'categoryText':data[cat]['text']
                    }
                    for k in data[cat]['actions'][action].keys():
                        rec['action.'+k]=data[cat]['actions'][action][k]
                    self.newItem(rec['action.name'],rec)
        else:
            self.newItem()
        
        
        
        self.exec()
        return self.data

class PluginGeneratorDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.plan=[]
        self.respath = Krita.instance().readSetting('','ResourceDirectory','')

        self.centralWidget = uic.loadUi( os.path.join(os.path.dirname(os.path.realpath(__file__)),'PluginGeneratorWidget.ui') )
        layout = QVBoxLayout()
        layout.addWidget(self.centralWidget)

        self.setLayout(layout)
        
        f = open( os.path.join(os.path.dirname(os.path.realpath(__file__)),'PluginGeneratorTemplates', 'index.json') )
        self.templates = json.load( f )
                    
        for tpl in self.templates:
            item = QListWidgetItem(tpl['name'] + ' - ' + tpl['text'])
            item.setToolTip( os.path.join(os.path.dirname(os.path.realpath(__file__)),'PluginGeneratorTemplates', tpl['name'].replace(' ','')) )
            self.centralWidget.templateListWidget.addItem(item)
            
        
        
        
        
        
        self.centralWidget.hotkeysBtn.setToolTip( json.dumps({'Scripts': {'text': 'My Scripts', 'actions': [{'activationConditions': '0', 'activationFlags': '10000', 'iconText': '', 'isCheckable': 'false', 'name': 'myAction', 'shortcut': '', 'statusTip': '', 'text': 'My Script', 'toolTip': '', 'whatsThis': '', 'category': 'Scripts', 'categoryText': 'My Scripts'}]}},indent=2) )
       
        self.centralWidget.projectPathBtn.clicked.connect(self.projectPath)
        self.centralWidget.setupGitBtn.clicked.connect(self.gitRemotePath)
        self.centralWidget.hotkeysBtn.clicked.connect(self.genActions)
        self.centralWidget.doneBtn.clicked.connect(self.doneClicked)
        
        self.centralWidget.autocompleteChk.stateChanged.connect(self.autocompleteCheck)        
        
        result = subprocess.run(['git --version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if b'git version' in result.stdout and not result.stderr:
            self.centralWidget.setupGitChk.setEnabled(True)
            self.centralWidget.setupGitBtn.setEnabled(True)
        else:
            self.centralWidget.setupGitChk.setEnabled(False)
            self.centralWidget.setupGitBtn.setEnabled(False)


    def doneClicked(self):
        res = self.buildPlan()

        if 'error' in res:
            QMessageBox.warning(self, "Error", res['error'])
        elif 'success' in res:
            QMessageBox.about(self, "Done!", "Plugin Created! Please restart Krita")
            self.close()

    def buildActionCollection(self,data):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<ActionCollection version="2" name="Scripts">'
        
        for cat in data.keys():
            xml+='\n <Actions category="'+cat+'">'
            xml+='\n  <text>'+data[cat]['text']+'</text>'
            
            for action in range(0,len(data[cat]['actions'])):
                xml+='\n <Action name="'+data[cat]['actions'][action]['name']+'">'
                for k in data[cat]['actions'][action].keys():
                    if k != 'name':
                        xml+='\n  <'+k+'>'+str(data[cat]['actions'][action][k])+'</'+k+'>'
                xml+='\n </Action>'
            
            xml+='\n </Actions>'

    
        xml+='\n</ActionCollection>'
        
        #print ("XML", xml)
        return xml
    
    def buildPlan(self):
        projectPath = self.centralWidget.projectPathLabel.text()
        if projectPath == 'Select Path...' or not os.path.isdir(projectPath):
            return { 'error':"Invalid 'Project Path'" }
        shortName = self.centralWidget.shortNameEdit.text()
        if shortName == '' or re.search(r'[^a-zA-Z0-9_]', shortName):
            return { 'error':"Invalid 'Short Name', stick to 'a-zA-Z0-9_' characters" }
        pluginTitle = self.centralWidget.titleEdit.text()
        if pluginTitle == '':
            return { 'error':"Invalid 'Plugin Title'" }
        shortDesc = self.centralWidget.shortDescEdit.text()
        if shortDesc == '':
            return { 'error':"Invalid 'Short Description'" }
        template = self.centralWidget.templateListWidget.currentItem()
        if not template:
            return { 'error':"No template was selected" }
                      
        projectRoot = os.path.join(projectPath,shortName)
             
        self.plan.append([ lambda: os.mkdir(projectRoot), "Create Directory "+projectRoot ])
        
        projectDesktopFile = os.path.join(projectRoot,shortName+'.desktop')
        projectDesktopFileContent = '''[Desktop Entry]
Type=Service
ServiceTypes=Krita/PythonPlugin
X-KDE-Library=%s
X-Python-2-Compatible=false
X-Krita-Manual=Manual.html
Name=%s
Comment=%s''' % (shortName, pluginTitle, shortDesc)
        self.plan.append([ lambda: self.writeToFile(projectDesktopFile,projectDesktopFileContent), "Create File "+projectDesktopFile+" with the following content:\n"+projectDesktopFileContent ])
        
        projectFolderPath = os.path.join(projectRoot,shortName)
        self.plan.append([ lambda: os.mkdir(projectFolderPath), "Create Directory "+projectFolderPath ])
        
        projectManualFile = os.path.join(projectFolderPath,'Manual.html')
        projectManualContent = self.centralWidget.manualTextEdit.toPlainText()
        self.plan.append([ lambda: self.writeToFile(projectManualFile,projectManualContent), "Create File "+projectManualFile+" with the following content:\n"+projectManualContent ])
        
        autocomplete='from krita import *'
        if self.centralWidget.autocompleteChk.isChecked():
            getAPI = GetKritaAPI()
            ver = (Krita.instance().version().split('-'))[0]

            projectAutoCompleteFile = os.path.join(projectFolderPath,'PyKrita.py')
            projectAutoCompleteContent = getAPI.genAutoComplete(ver)
            self.plan.append([ lambda: self.writeToFile(projectAutoCompleteFile,projectAutoCompleteContent), "Generating Auto Complete File: "+projectAutoCompleteFile ])
            autocomplete = '''
# load autocomplete
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .PyKrita import *
else:
    from krita import *
            '''
        
        self.plan.append([ lambda: self.genTemplate( template.toolTip(), {
            'SHORTNAME':shortName,
            'PLUGINTITLE':pluginTitle,
            'PROJECTROOT':projectRoot,
            'AUTOCOMPLETE':autocomplete
            },projectFolderPath), "Copying template "+template.toolTip()+" to "+projectFolderPath])
        
        if self.centralWidget.hotkeysChk.isChecked():
            projectActionFile = os.path.join(projectRoot,shortName+'.action')
            projectActionContent = self.buildActionCollection( json.loads(self.centralWidget.hotkeysBtn.toolTip()) )
            self.plan.append([ lambda: self.writeToFile(projectActionFile,projectActionContent), "Create File "+projectActionFile+" with the following content:\n"+projectActionContent ])
        
        if self.centralWidget.setupGitChk.isChecked():
            readmeFile = os.path.join(projectRoot,'README.md')
            self.plan.append([ lambda: self.writeToFile(readmeFile,projectManualContent), "Create File "+readmeFile+" with the following content:\n"+projectManualContent ])
            self.plan.append([ lambda: subprocess.run(['git init '+projectRoot], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True), "Creating local git with: git init "+projectRoot ])
            gitRemotePath = self.centralWidget.setupGitChk.toolTip()
            if gitRemotePath:
                self.plan.append([ lambda: subprocess.run(['cd "'+projectRoot+'" && git remote add origin '+gitRemotePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True), 'Creating local git with: cd "'+projectRoot+'" && git remote add origin '+gitRemotePath ])
            
        if self.centralWidget.projectPathSymlinkChk.isChecked():
            symlinkFolder = os.path.join(self.respath,'pykrita',shortName)
            self.plan.append([ lambda: os.symlink(projectFolderPath,symlinkFolder), "Symlinking "+projectFolderPath+" to "+symlinkFolder ])
            self.plan.append([ lambda: os.symlink(projectFolderPath+'.desktop',symlinkFolder+'.desktop'), "Symlinking "+projectFolderPath+".desktop to "+symlinkFolder+'.desktop' ])
            if self.centralWidget.hotkeysChk.isChecked():
                symlinkActionFolder = os.path.join(self.respath,'actions',shortName)
                self.plan.append([ lambda: os.symlink(projectFolderPath+'.action',symlinkActionFolder+'.action'), "Symlinking "+projectFolderPath+".action to "+symlinkActionFolder+'.action' ])
        
        
        
        
        self.plan.append([lambda: Application.writeSetting(
                'python',
                'enable_%s' % shortName,
                'true'), "Activate Plugin in Plugin Manager"])
        
        confirmActions=''            
        for item in self.plan:
             confirmActions+=item[1]+"\n\n"
        
        
        _ignore, ok = QInputDialog.getMultiLineText(self,"Confirm","The following work will be executed:",confirmActions)
        if ok:
            for step in self.plan:
                print ("Generating Step:", step[1])
                step[0]()
            return { 'success':"Done!" }
        else:
            return {}

    def genTemplate(self,tpl,v,outputPath=None):
        def vsub(p):
            return v[p.group(1)]
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),'PluginGeneratorTemplates',tpl)
        

        for dp, dn, filenames in os.walk( folder ):
            for fn in filenames:
                f = open( os.path.join(dp,fn), "r")
                fileContent = f.read()
                fn = fn.replace('[SHORTNAME]',v['SHORTNAME'])
                
                fileContent=re.sub(r"'''\[\%([A-Z0-9]+?)\%\]'''", vsub, fileContent)
                
                if outputPath:
                    self.writeToFile(os.path.join(outputPath,fn), fileContent)
                else:
                    print ("Template Output:", os.path.join(outputPath,fn), fileContent)
                f.close()

        
    def genActions(self):
        d = json.loads(self.centralWidget.hotkeysBtn.toolTip()) if self.centralWidget.hotkeysBtn.toolTip() else None
        
        d = ActionGeneratorDialog().getData( d )
        #print ("Data", d)
        self.centralWidget.hotkeysBtn.setToolTip(json.dumps(d, indent=2))
        
    def gitRemotePath(self):
        url, ok = QInputDialog.getText(self, 'Git Remote Path', 'Remote path to git repository:')
        if ok:
            self.centralWidget.setupGitChk.setToolTip(url)
                
        
    def projectPath(self):
        destDir = QFileDialog.getExistingDirectory(None, 'Select Project Directory',QDir.homePath(), QFileDialog.ShowDirsOnly)
        self.centralWidget.projectPathLabel.setText(destDir)

    def writeToFile(self,path,s):
        f = open(path, 'w')
        n = f.write(s)
        f.close()
    def autocompleteCheck(self, state):
        if state == Qt.Checked:
            if not self.downloadKritaAPI():
                self.centralWidget.autocompleteChk.setChecked(False)

    def downloadKritaAPI(self):
        ver = (Krita.instance().version().split('-'))[0]
        respath = Krita.instance().readSetting('','ResourceDirectory','')
        if respath == '':
            respath = os.path.dirname(os.path.realpath(__file__))
        else:
            respath=os.path.join(respath,'pykrita','PluginDevTools')
            
        if os.path.isfile(respath + ".KritaAPI."+ver+".zip"):
            return True
        msgbox = QMessageBox(QMessageBox.Question,'Would you like to download the API details automatically?',
                                '', QMessageBox.Yes | QMessageBox.No)
        msgbox.setTextFormat(Qt.RichText)

        msgbox.setText("""Developer Tools would like to connect to the internet to download Krita API details.
This process will only access Krita's offical git repository at invent.kde.org.
<hr>
The API is still accessable even without downloading this file, but may not be fully complete, no documentation will be available and you will not be able to generate autocomplete files.
<hr>
You can also do this manually by downloading the following (Unless you are on Krita Next nightly, 'master' should be replaced with the tag you plan to target, ex. 'v"""+ver+"""' or 'v"""+ver+"""-beta1'):<br>
<u>https://invent.kde.org/graphics/krita/-/archive/master/krita-master.zip?path=libs/libkis</u>
<br>
And place it in:<br>
<u>""" + respath + """.KritaAPI."""+ver+""".zip</u>
<hr>
This only needs to be done once per new version of Krita. Do note that Krita may freeze up for about a minute.
<hr>
Would you like to download the API details(less than 200kb of data) automatically?
""")

        if msgbox.exec() == QMessageBox.Yes:
            getAPI = GetKritaAPI()
            res = {}
            try:
                res=getAPI.updateData(ver)
            except:
                QMessageBox(QMessageBox.Warning,'Failed!', "Failed to download API details! Make sure you have internet connection and your python urlib ssl is working properly").exec()
                return False
            print ("RES", res)

            if res['status'] == 0:
                msgbox = QMessageBox(QMessageBox.Warning,'Error',str(res['error']))

                msgbox.exec()
                return False
            else:
                QMessageBox(QMessageBox.Information,'Success!', "API details have been downloaded successfully!").exec()
        else:
            return False


        return True
