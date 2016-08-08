import urllib2, os, sys
from termcolor import colored
import json

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
check_completed=True
ci_test=False

ignore_streams = ''

def loadIgnoreStreams() :
    global ignore_streams
    content = fread(os.path.join(LOCAL_DIR, '.test', 'ignore_streams.json'))
    ignore_streams = json.loads(content)

def checkLink(page, filepath):
    url = page      
    ignored = filepath.replace(LOCAL_DIR,"") in ignore_streams['ignore']
    c = 'green' if ignored else 'red'
    try:                                                                 
        req = urllib2.Request(url ,None) 
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Language', 'nl,en-US;q=0.7,en;q=0.3')
        req.add_header('Accept-Encoding', 'deflate')
        #req.add_header('Connection', 'keep-alive')
        response = urllib2.urlopen(req, timeout=5)                                            
        if response.code != 200 :
            print colored("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (Response code: "+str(response.code)+")", color=c)
            return ignored
        else :
            return True
    except urllib2.HTTPError as http_error :
        print colored("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (http code: "+str(http_error.code)+")", color=c)
        return ignored
    except urllib2.URLError as url_error :
        print colored("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (reason: "+ str(url_error.reason) +")",color=c)
        return ignored
    except :                                                                                       
        print colored("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect ("+page+")",color=c)
        print colored(sys.exc_info()[0],c)
        return ignored
    return False
        
def browse(strDir):
    global check_completed
    global ci_test
    for directory in getDirs(strDir) :
        browse(os.path.join(strDir,directory))
    for file in getFiles(strDir) :
        if(file[-5:] == '.strm') :
            if strDir == os.path.join(LOCAL_DIR,'streams','--Webcams--') :
                checkLink(fread(os.path.join(strDir, file)), os.path.join(strDir, file))
            else :
                if not checkLink(fread(os.path.join(strDir, file)), os.path.join(strDir, file)) :
                    if ci_test :
                        check_completed=False
                    
def getDirs(strRoot) :
    dirs = list()
    dirList = os.listdir(strRoot)
    for directory in dirList:
        if os.path.isdir(os.path.join(strRoot, directory)) == True:
            dirs.append(directory)
    dirs.sort()
    return dirs

def getFiles(strRoot) :
    files = list()
    dirList = os.listdir(strRoot)
    for directory in dirList:
        if os.path.isdir(os.path.join(strRoot, directory)) != True:
            files.append(directory)
    files.sort()
    return files
    
def fread(filename):
    with open(filename) as f:
        return f.read()


loadIgnoreStreams()

if len(sys.argv) == 1:
    browse(os.path.join(LOCAL_DIR, 'streams'))
else :
    if len(sys.argv) == 2 :
        if sys.argv[1] == 'ci':
            ci_test = True
            browse(os.path.join(LOCAL_DIR, 'streams'))
            if not check_completed :
                sys.exit(1)
        else :
            browse(sys.argv[1])
    else :
        print "usage "+sys.argv[0]+" [/path/to/streams]"

