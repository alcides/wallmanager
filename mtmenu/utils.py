from models import *
from window_manager import *

def get_applications(cat=None, sort_by_value=False):
    if cat: 
        return get_applications_of_category(cat, sort_by_value)
    else:
        return get_all_applications(sort_by_value)


def get_all_categories():
    return CategoryProxy.objects.all()    

    
def get_all_applications(sort_by_value=False):
    return sort_apps(ApplicationProxy.objects.all(), sort_by_value)


def get_applications_of_category(cat, sort_by_value=False):
        return sort_apps( ApplicationProxy.objects.filter(category = cat), sort_by_value )
    

def exists_category(category_name):
    return len(CategoryProxy.objects.filter(name = category_name)) > 0


def sort_apps(apps, sort_by_value):
    if sort_by_value:
        return sorted(list(apps), key = lambda app: app.value(), reverse= True)
    else:
        return apps.order_by('name')
    
def bring_window_to_front(hwnd = None):
    ''' Bring the WallManager window to the front'''
    
    if hwnd == None:
        from mtmenu import self_hwnd
        hwnd = self_hwnd
    
    w = WindowMgr(hwnd)
    for win in w.getWindows():
        print win
    #w.find_window_wildcard()
    #w.set_foreground()
