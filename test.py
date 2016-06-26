import urllib2, os, sys

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

def checkLink(page, filepath):
    url = page                                                           
    try:                                                                 
        req = urllib2.Request(url ,None) 
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Language', 'nl,en-US;q=0.7,en;q=0.3')
        req.add_header('Accept-Encoding', 'deflate')
        #req.add_header('Connection', 'keep-alive')
        response = urllib2.urlopen(req, timeout=5)                                            
        if response.code != 200 :
            print("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (Response code: "+str(response.code)+")")       
    except urllib2.HTTPError as http_error :
        print("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (http code: "+str(http_error.code)+")")
    except urllib2.URLError as url_error :
        print("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect (reason: "+ str(url_error.reason) +")")
    except :                                                                                       
        print("- [ ] Stream in " + filepath.replace(LOCAL_DIR,"") + " seems incorrect ("+page+")")
        print(sys.exc_info()[0])
        
def browse(strDir):
    for directory in getDirs(strDir) :
        browse(os.path.join(strDir,directory))
    for file in getFiles(strDir) :
        if(file[-5:] == '.strm') :
            checkLink(fread(os.path.join(strDir, file)), os.path.join(strDir, file))

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

if len(sys.argv) == 1:
    browse(os.path.join(LOCAL_DIR, 'streams'))
else :
    if len(sys.argv) == 2 :
        browse(sys.argv[1])
    else :
        print "usage "+sys.argv[0]+" [/path/to/streams]"
