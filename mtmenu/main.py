from pymt import *
from ui.mainwindow import MainWindow
from gesture.gesture_scan import GestureScan
from proxy import *
from pymt.ui.window.win_glut import MTWindowGlut
from models import ApplicationProxy
from mtmenu.models import CategoryProxy
from utils import *
from ui import *


if __name__ == '__main__':
    # Start TUIO proxy
    proxy.start()
    
    main_window = MainWindow(width=800, height=600)

    apps_grid.add( getAllApplications() )
    category_grid.add( getAllCategories() )

    # Add appsList to Scatter
    scatter.add_widget(apps_grid)
    scatter.add_widget(category_grid)
    
    # Add Scatter to MainWindow
    main_window.add_widget(scatter)
    
    #Add gesture recognition
    main_window.add_widget(GestureScan())
    
    
    # Execute main loop
    runTouchApp()
