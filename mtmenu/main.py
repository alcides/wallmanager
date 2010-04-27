from pymt import *
from ui.mainwindow import MainWindow
from ui.appslist import AppsList
from ui.appbutton import AppButton
from ui.categorybutton import CategoryButton
from ui.categorylist import CategoryList
from gesture.gesture_scan import GestureScan
from proxy import *
from pymt.ui.window.win_glut import MTWindowGlut
from models import ApplicationProxy
from mtmenu.models import CategoryProxy


if __name__ == '__main__':
    # Start TUIO proxy
    proxy.start()
    
    
    main_window = MainWindow(width=800, height=600)
    
    # Construct AppsList looping through all apps
    apps_grid = AppsList(pos=(200,20), size=(460,460))
    
    all_apps = getAllApplications()

    style = {'bg-color': (0, .2, 0, 1), 'draw-background': 1}
    for app in all_apps:
        item = AppButton(app, style=style)
        apps_grid.add_widget(item)
        
        
    category_grid = CategoryList()
    
    '''categories = getCategories()
    for category in getCategories():
        category_grid.add_widget( CategoryButton(label = category,name, style=style) )
    '''    
    category_grid.add_widget( CategoryButton(label = 'ALL', style=style) )
    
    from ui import scatter
    
    # Add appsList to Scatter
    scatter.add_widget(apps_grid)
    scatter.add_widget(category_grid)
    
    # Add Scatter to MainWindow
    main_window.add_widget(scatter)
    
    #Add gesture recognition
    main_window.add_widget(GestureScan())
    
    
    # Execute main loop
    runTouchApp()
