import os, sys, urlparse
import xbmc, xbmcaddon

from lib import xbmcutil

args = urlparse.parse_qs(sys.argv[2][1:])

addon_handle=int(sys.argv[1])
xbmcutil.addon_handle=addon_handle

__settings__ = xbmcaddon.Addon(id='plugin.audio.nlradio')
rootDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')
streamDir = os.path.join(rootDir, "streams")

def browse(strDir):
    for directory in getDirs(strDir) :
        xbmcutil.addMenuItem('[COLOR orange]'+directory+'[/COLOR]', os.path.join(strDir, directory), 'false')
    for file in getFiles(strDir) :
        if(file[-5:] == '.strm') :
            background = os.path.join(rootDir, 'fanart.jpg')
            if(os.path.isfile(os.path.join(strDir, file[:-5]+'.tbn'))) :
                iconFile = os.path.join(strDir, file[:-5]+'.tbn')
            else :
                iconFile = os.path.join(rootDir, 'icon.png')
            xbmcutil.addMenuItem(file[:-5], os.path.join(strDir, file), 'true', icon=iconFile, fanart=background)
    xbmcutil.endOfList()

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
        if os.path.isdir(os.path.join(strRoot, directory)) == True:
            print('')
        else :
            files.append(directory)
    files.sort()
    return files
    
argBrowse = args.get('browse', None)

if argBrowse is not None :
    browse(argBrowse[0])
else:
    browse(streamDir)
