from pymt import *
from gesture.gesture_scan import GestureScan
from mtmenu.proxy import *
from pymt.ui.window.win_glut import MTWindowGlut
from mtmenu.models import ApplicationProxy, CategoryProxy
from mtmenu.utils import *
from mtmenu.ui import *
from mtmenu.ui.imagebutton import ImageButton
from mtmenu.settings import SCATTER_SIZE
from mtmenu.ui.popup import Popup


if __name__ == '__main__':
    # Start TUIO proxy
    proxy.start()

    apps_grid.add( getAllApplications() )
    category_grid.add( getAllCategories() )
    
    # Top left logo
    logo = MTScatterWidget(size=(350,68), pos= (40,SCATTER_SIZE[1]- 68))
    logo.add_widget( MTScatterImage(filename= 'images/logo.png', pos=(0,0), scale= 0.5) ) #icon
    logo.add_widget( MTLabel(label='SenseWall', pos= (60, 14), font_size= 40) ) #main_label
    logo.add_widget( MTLabel(label='http://sensewall.dei.uc.pt', pos= (60, 0), font_size= 16) ) #other label
    scatter.add_widget( logo )

    # Top right help icon
    help = MTScatterWidget(size=(60,60), pos= (SCATTER_SIZE[0]-65, SCATTER_SIZE[1]-65))
    help.add_widget( ImageButton(filename= 'images/help.png', scale= 0.9) )
    scatter.add_widget( help )
    


    # Add widgets to Scatter
    scatter.add_widget(apps_grid)
    scatter.add_widget(category_grid)
    
    # Add Scatter to MainWindow
    main_window.add_widget(scatter)
    
    #Add gesture recognition
    main_window.add_widget(GestureScan())
    
    
    # Execute main loop
    runTouchApp()
