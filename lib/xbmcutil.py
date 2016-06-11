import sys
import xbmcgui, xbmcplugin

	
def addMenuItem(strName, strUrl, bIsPlayable='true', icon=None, fanart=None):
    li = xbmcgui.ListItem(strName)
    if not icon is None :
        iconPath = icon
        li = xbmcgui.ListItem(label=strName, iconImage=iconPath, thumbnailImage=iconPath)
    else :
        li = xbmcgui.ListItem(strName)
    if not fanart is None :
        fanartimg = fanart
        li.setProperty('fanart_image',fanartimg)
    li.setProperty('IsPlayable', bIsPlayable)
    li.addContextMenuItems([ ('Vernieuwen...', 'Container.Refresh') ])
    if bIsPlayable == 'true':
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=strUrl, listitem=li)
    else :
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=sys.argv[0]+'?browse='+strUrl, listitem=li, isFolder=True)

def endOfList():
    xbmcplugin.endOfDirectory(addon_handle)