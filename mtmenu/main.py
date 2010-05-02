from pymt import *
from ui.mainwindow import MainWindow
from gesture.gesture_scan import GestureScan
from mtmenu.proxy import *
from pymt.ui.window.win_glut import MTWindowGlut
from mtmenu.models import ApplicationProxy, CategoryProxy
from mtmenu.utils import *
from mtmenu.ui import *


if __name__ == '__main__':
    # Start TUIO proxy
    proxy.start()
    
    main_window = MainWindow(width=800, height=600)

    apps_grid.add( getAllApplications() )
    category_grid.add( getAllCategories() )
    
    # Top left logo
    icon = MTScatterImage(filename= 'images/logo.png', pos=(40,580), scale= 0.5)
    main_label =  MTLabel(label='SenseWall', pos= (100, 590), font_size= 40)
    secondary_label = MTLabel(label='http://sensewall.dei.uc.pt', pos= (100, 578), font_size= 16)


    # Add widgets to Scatter
    scatter.add_widget(apps_grid)
    scatter.add_widget(category_grid)
    scatter.add_widget( icon )
    scatter.add_widget( main_label )
    scatter.add_widget( secondary_label )
    
    # Add Scatter to MainWindow
    main_window.add_widget(scatter)
    
    #Add gesture recognition
    main_window.add_widget(GestureScan())
    
    
    # Execute main loop
    runTouchApp()
