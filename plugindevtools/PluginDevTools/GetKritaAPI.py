import urllib
import urllib.request
import zipfile
import json
import http.client
import socket
import ssl
import time
import re
import io
import os
import krita
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

class GetKritaAPI(QObject):
    
    MAP_TYPES = {
        'QStringList': ['List[str]'],
        'QString': ['str'],
        'qreal': ['float'],
        'double': ['float'],
        'QByteArray': ['Union[QByteArray, bytes, bytearray]','QByteArray'],
        'QList':['List'],
        'QVector':['List'],
        'QMap':['Dict'],
        'true':['True'],
        'false':['False'],
        'void': ['None']
        }
    
    DECLARE_CLASS = {
        'Document': 'Krita.instance().activeDocument()',
        'Node': 'Krita.instance().activeDocument().activeNode()'
        }

   
    def updateData(self, kritaVersion, defaultTimeout = 5):
        headers = {
            'Accept': '*/*',
            "User-Agent": "Krita-DevTools Plugin"
        }


        # Get List of tags and confirm if IPv6 is working properly
        tagList = "https://invent.kde.org/api/v4/projects/graphics%2Fkrita/repository/tags"

        s1 = time.time()
        req = urllib.request.Request(tagList, headers=headers)
        with urllib.request.urlopen(req, timeout=defaultTimeout) as source:
            if time.time() - s1 > defaultTimeout:
                ForceIPv4Connection()
                defaultTimeout += 25

            try:
                jres = json.loads(source.read())

                tag = 'master'
                
                for tagDict in jres:
                    if (tagDict['name'].split('-'))[0] == 'v'+ kritaVersion:
                        tag = tagDict['name']
                        
                # Figure out when API was last updated
                lastCommit = "https://invent.kde.org/api/graphql"

                urldata={"query":"query pathLastCommit($projectPath: ID!, $path: String, $ref: String!) {\n  project(fullPath: $projectPath) {\n    id\n    __typename\n    repository {\n      __typename\n      tree(path: $path, ref: $ref) {\n        __typename\n        lastCommit {\n          __typename\n          sha\n          title\n          titleHtml\n          descriptionHtml\n          message\n          webPath\n          authoredDate\n          authorName\n          authorGravatar\n          author {\n            __typename\n            name\n            avatarUrl\n            webPath\n          }\n          signatureHtml\n          pipelines(ref: $ref, first: 1) {\n            __typename\n            edges {\n              __typename\n              node {\n                __typename\n                detailedStatus {\n                  __typename\n                  detailsPath\n                  icon\n                  tooltip\n                  text\n                  group\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"projectPath":"graphics/krita","ref":tag,"path":"libs/libkis"}}
                

                req = urllib.request.Request(lastCommit, headers=headers)
                req.add_header('Content-Type', 'application/json; charset=utf-8')
                jsondata = json.dumps(urldata)
                jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
                req.add_header('Content-Length', len(jsondataasbytes))
                
                with urllib.request.urlopen(req, jsondataasbytes, timeout=defaultTimeout) as source:
                    jres = json.loads(source.read())
                    date = jres['data']['project']['repository']['tree']['lastCommit']['authoredDate']

                    # Download the API details
                    zipUrl = 'https://invent.kde.org/graphics/krita/-/archive/'+tag+'/krita-'+tag+'.zip?path=libs/libkis'
                    req = urllib.request.Request(zipUrl, headers=headers)
                    with urllib.request.urlopen(req, timeout=defaultTimeout) as source:
                        data = source.read()
                        with zipfile.ZipFile(io.BytesIO(data)) as myzip:
                            if 'krita-'+tag+'-libs-libkis/libs/libkis/Window.h' in myzip.namelist():
                                respath = Krita.instance().readSetting('','ResourceDirectory','')
                                if respath == '':
                                    respath = os.path.dirname(os.path.realpath(__file__))
                                else:
                                    respath=os.path.join(respath,'pykrita','PluginDevTools')
                                with open( respath + '.KritaAPI.'+kritaVersion+'.zip', 'wb') as f:
                                    f.write(data)
                                    f.close()
                                    return { 'status': 1, 'data': { 'updated': date } }
                                    
                            else:
                                raise Exception("Archive is invalid.")
    

                    
            except Exception as e:
                
                return { 'status':0, 'error': str(e) }

    
    def parseData(self, kritaVersion):
        mapDict = {}
        respath = Krita.instance().readSetting('','ResourceDirectory','')
        if respath == '':
            respath = os.path.dirname(os.path.realpath(__file__))
        else:
            respath=os.path.join(respath,'pykrita','PluginDevTools')
        with zipfile.ZipFile( respath + '.KritaAPI.'+kritaVersion+'.zip' ) as myzip:
            for fn in myzip.namelist():
                if fn.endswith('.h') and '/Test/' not in fn:
                    content = str(myzip.read(fn),'utf-8')
                    className = re.search(r'^.*[/\\](.+?)\.h$', fn).group(1)
                    
                    #print ("CLASSNAME", className)
                    
                    #print ( content )
                    regexFile = re.compile(r"^(?:.+?\/\*\*\s*(.+?)\s*\*\/.*?|.+?)\n\s*?class KRITALIBKIS_EXPORT (\w+)\s*?[\:\n]\s*(?:public\s+|)(\w+|)", re.DOTALL)
                    
                    match = regexFile.search(content)
                    content = regexFile.sub('', content)
                    #print ( content )

                    regexClass = re.compile(r"\n\s*?(public|private)\s*(Q_SLOTS|)\s*:\s*?\n(.+?)(\n\s*?(?:public|private)\s*(?:Q_SLOTS|)\s*:\s*?\n|\#endif \/\/ LIBKIS_)", re.DOTALL)
                    
                    regexMethod = re.compile(r"^(?:.+?(?P<doc>\/\*\*\s*.+?\s*\*\/|\/\/\/[^\r\n]+?)\s*?|\s+?)\n\s*?(?:(?P<type>(?:virtual|static|)\s*?[\w\*]+(?:\<[\w \*,]+\>|))\s+(?P<name>[\w\*]+)|(?P<cname>"+className+r"))\((?P<params>[^\r\n]*)\)(?P<extra>[^\r\n])*?;", re.DOTALL)
                    
                    regexParam = re.compile(r'(?:^|\s)(\S+?(?:\<.+?\>|))\s*[\&\*]*(\w+?)(?:\s*=\s*(.+?)|)\s*$', re.DOTALL)
                    
                    if match:
                        #print( "match=",match.group(2), match.group(1) )
                        modName = match.group(2)
                        doc = match.group(1) if match.group(1) else ''
                        doc = re.sub(r'^\s*(?:/\*\*|///)\s*\**', r'', doc)
                        doc = re.sub(r'/\s*$', r'', doc)
                        doc = re.sub(r'\n\s*?\* \@', r'\n@', doc )
                        start = doc.find('@code')

                        if start > -1:
                            end = doc.find('@endcode',start)
                            doc = doc.replace( doc[start:end],re.sub(r'\n\s*?\* ',r'\n', doc[start:end]))
                
                        doc = re.sub(r'\n\s*?\*', r'', doc )
                        mapDict[modName] = { 'doc':doc, 'methods':{}, 'declare':[], 'parent':match.group(3)  }
                        if modName in self.DECLARE_CLASS:
                            mapDict[modName]['declare'].append({ 
                                'doc': self.DECLARE_CLASS[modName], 
                                'return': className, 
                                'params': [], 
                                'access': '' 
                            })
                    
                    while True:
                        match = regexClass.search(content)
                        if match is not None:
                            
                            #print ( "matchMethod", match.group(1), match.group(2), match.group(3) )
                            content = regexClass.sub(match.group(4), content, 1)
                            
                            methodAccess = match.group(1) + " " + match.group(2)
                            subcontent = match.group(3)
                            
                            while True:
                                matchMethod = regexMethod.search(subcontent)
                                subcontent = regexMethod.sub('', subcontent, 1)
                                if matchMethod:
                                    #if matchMethod.group('cname'): print ("CNAME!", matchMethod.group('cname') )
                                    docMethod = matchMethod.group('doc') if matchMethod.group('doc') else ''
                                    docMethod = re.sub(r'^\s*(?:/\*\*|///)\s*\**', r'', docMethod)
                                    docMethod = re.sub(r'/\s*$', r'', docMethod)
                                    docMethod = re.sub(r'\n\s*?\* \@', r'\n@', docMethod)
                                    start2 = docMethod.find('@code')
                                    if start2 > -1:
                                        #print ("SELECTION FOUND!")
                                        end2 = docMethod.find('@endcode',start2)
                                        docMethod = docMethod.replace( docMethod[start2:end2],re.sub(r'\n\s*?\* ',r'\n', docMethod[start2:end2]))
                                                
                                    docMethod = re.sub(r'\n\s*?\*', r'', docMethod )
                                    methName = (matchMethod.group('name') if matchMethod.group('name') else matchMethod.group('cname')).replace('*','')
                                    
                                    params = []
                                    #print ('mp', matchMethod.group('params'))
                                    paramText = matchMethod.group('params')
                                    if paramText:
                                        paramText = re.sub(r'\<(.*?),(.*?)\>',r'<\1&&\2>', paramText)
                                        for param in paramText.split(','):
                                            pmatch = regexParam.search(param)
                                            #print ( "p["+param+']', pmatch )
                                            params.append({ 
                                                'type': re.sub(r'\<(.*?)&&(.*?)\>',r'<\1,\2>', pmatch.group(1)), 
                                                'name': pmatch.group(2), 
                                                'optional': re.sub(r'\<(.*?)&&(.*?)\>',r'<\1,\2>', pmatch.group(3)) if pmatch.group(3) else None
                                                })
                                    #print ("met", className, methName, params)
                                    #if 'internal use only' in docMethod: continue
                                    if methName == modName:

                                        mapDict[modName]['declare'].append({ 
                                            'doc': docMethod, 
                                            'return': className if matchMethod.group('cname') else matchMethod.group('type'), 
                                            'params': params, 
                                            'access': methodAccess 
                                            })
                                    else:
                                        mapDict[modName]['methods'][methName]={
                                            'name': methName,
                                            'doc':docMethod, 
                                            'return': matchMethod.group('type').strip(), 
                                            'params': params, 
                                            'access': methodAccess 
                                            }
                                else:
                                    break
                            #print ("cont=",content)
                        else:
                            #print ("NO MATCH!")
                            break
                        
                        
                        #print ("cont=",content)
                        
                        #methods = decl.group(3)
                        
                        
        return mapDict
    
    def convertType(self, vtype, classKeys, param = True):
        for k in reversed(sorted(self.MAP_TYPES.keys())):
            v = self.MAP_TYPES[k]
            rv = v[0] if param or len(v) == 1 else v[1]
            if k == vtype:
                return rv
            elif k in vtype:
                vtype = vtype.replace(k, rv)
        
        vtype = vtype.replace('<','[').replace('>',']').replace(' *','').replace('*','').replace('&','').replace('virtual ','')
        
        #if param:
        for k in reversed(sorted(classKeys)):
            vtype = re.sub( r"(^|[\[\( ,])"+k, r"\1'"+k+"'", vtype)
        
        vtype = re.sub( r"((?:Kis|Ko)\w+)", r"'\1'", vtype)
        
        return vtype

    def genAutoComplete(self, kritaVersion):
        output = "from PyQt5.QtCore import *\nfrom PyQt5.QtGui import *\nfrom PyQt5.QtWidgets import *\nfrom typing import List, Dict, Union\n"
        parseData = self.parseData(kritaVersion)

        sortedLists = { 'QObject':[], 'Other':[] } 
        for k in reversed(sorted(parseData.keys())):
            v = parseData[k]
            
            if v['parent'] == 'QObject':
                sortedLists['QObject'].append( k )
            else:
                sortedLists['Other'].append( k )
                
            if v['parent'].startswith('Ko') or v['parent'].startswith('Kis'):
                output += v['parent']+" = QObject\n"
            
        
        
        for k in sortedLists['QObject'] + sortedLists['Other']:
            v = parseData[k]
            output += "class " + k + "(" + v['parent'] +"):\n"
            output += '\t"""' + v['doc'] + ' """\n\n'
            
            if v['declare']:
                paramList = ['self']
                
                for param in m['params']:
                    paramList.append( param['name'] + ": " + self.convertType(param['type'], parseData.keys() ) + (" = " + self.convertType(param['optional'], parseData.keys() ) if param['optional'] else "") )
                
                output += "\tdef __init__(" + ', '.join(paramList) + ") -> " + self.convertType(m['return'], parseData.keys() , False) +":\n"
                output += '\t\t"""' + m['doc'] + ' """\n\n'  
            
            for km, m in v['methods'].items():
                paramList = []
                paramNames = []
                
                #print ( "METHOD=", m )
                if "static" not in m['return']:
                    paramList.append('self')
                else:
                    m['return'] = m['return'].replace('static','')
                    output += "\t@staticmethod\n"
                
                for param in m['params']:
                    paramNames.append( param['name'] )
                    paramList.append( param['name'] + ": " + self.convertType(param['type'], parseData.keys() ) + (" = " + self.convertType(param['optional'], parseData.keys() ) if param['optional'] else "") )
                
                output += "\tdef " + m['name'] + "(" + ', '.join(paramList) + ") -> " + self.convertType(m['return'], parseData.keys() , False) +":\n"
                output += "\t\t# type: (" + ', '.join(paramNames) + ") -> " + self.convertType(m['return'], {}.keys() , False) +":\n"
                output += '\t\t"""@access ' + m['access'] + "\n" + m['doc'] + ' """\n\n'
            
        return output


class ForceIPv4Connection():
    def __init__(self, caller = None):
        super().__init__()
        urllib.request.HTTPSHandler = self.OverloadHTTPSHandler
        print ("overloaded!")

    class OverloadHTTPSConnection(http.client.HTTPSConnection):
        def connect(self):
            self.sock = socket.socket(socket.AF_INET)
            self.sock.connect((self.host, self.port))
            if self._tunnel_host:
                self._tunnel()
            self.sock = ssl.wrap_socket(self.sock, self.key_file, self.cert_file)



    class OverloadHTTPSHandler(urllib.request.AbstractHTTPHandler):

        def __init__(self, debuglevel=0, context=None, check_hostname=None):
            urllib.request.AbstractHTTPHandler.__init__(self, debuglevel)
            self._context = context
            self._check_hostname = check_hostname

        def https_open(self, req):
            return self.do_open(ForceIPv4Connection.OverloadHTTPSConnection, req,
                context=self._context, check_hostname=self._check_hostname)

        https_request = urllib.request.AbstractHTTPHandler.do_request_


