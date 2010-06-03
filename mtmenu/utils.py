import sys
sys.path.append('..')
sys.path.append('../webmanager')

from time import sleep

from pymt import *
from models import *
from window_manager import *
from config import MAX_ATTEMPTS, SLEEP_SECONDS_BETWEEN_ATTEMPTS, NATIVE_APP_NAMES, PRODUCTION
from mtmenu import logger



def get_applications(cat=None, sort_by_value=False):
    if cat: 
        return get_applications_of_category(cat, sort_by_value)
    else:
        return get_all_applications(sort_by_value)


def get_all_categories():
    return CategoryProxy.objects.all().order_by('-name') 

    
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
    
def bring_window_to_front(toApp = False):
    ''' Bring the WallManager window to the front'''
    from mtmenu import self_hwnd
    
    hwnd = None
    
    w = WindowMgr()
    if toApp:
        
        for i in range(MAX_ATTEMPTS):
            # loop for the open windows on the desktop
            for handler, name in w.getWindows():
                logger.debug("Window opened with name %s" % name)
                if handler != self_hwnd and name not in NATIVE_APP_NAMES:
                    hwnd = handler
                    logger.info('Changing context to handler %d with name %s' % (handler, name))
                    break
            if hwnd != None:
                break
            sleep(SLEEP_SECONDS_BETWEEN_ATTEMPTS)
        
        logger.debug("Got handler %d" % hwnd)    
        if hwnd == None:
            hwnd = self_hwnd
            
    else:
        hwnd = self_hwnd
        logger.info("Going back to the main application")
        
        for handler, name in w.getWindows():
            logger.debug("Window opened with name %s" % name)
            if handler != self_hwnd and name not in NATIVE_APP_NAMES:
                
                tid, pid = win32process.GetWindowThreadProcessId(handler)
                if PRODUCTION:
                    Popen("taskkill /F /T /PID %i" % pid, shell=True)
                
                logger.debug('killing %s with PID %d' % (name, pid))
        
    w.set_foreground(hwnd)

def get_trimmed_label_widget(text, position, font_size, max_width):
    """ Constructs an MTLabel with a max_width. If needed label text is trimmed 
    and '...' is added for the user to known that more text exists.
    
    Return: list(label_object, label_text_after_trim) """
    
    text_changed = False
    label_obj = MTLabel(label = text,
                        pos = position,
                        font_size = font_size,
                        autowidth = True)
    
    while label_obj.width > max_width:
    
        text = text[:-1]
        
        text_changed = True
        label_obj = MTLabel(label = "%s..." % text,
                            pos = position,
                            font_size = font_size,
                            autowidth = True)
    
    if text_changed:
        text = "%s..." % text
    
    return (label_obj, text)
