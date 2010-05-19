import sys
sys.path.append("..")

from pymt import *
from mtmenu import *
from utils import last_activity_checker
from gesture.gesture_scan import GestureScan

if __name__ == '__main__':
    
    # TUIO proxy
    proxy.start()
    
    # BACKGROUND
    main_window.add_widget(background_image)
    
    # TOPBAR
    main_window.add_widget(top_bar)
    
    # APPSLIST
    main_window.add_widget(apps_list)
    
    # CATEGORIES LIST
    main_window.add_widget(categories_list)
    
    # GESTURE
    main_window.add_widget(GestureScan())
    
    # Call inactivity checker
    last_activity_checker()
    
    
    runTouchApp()
