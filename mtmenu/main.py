from pymt import *
from gesture.gesture_scan import GestureScan
from mtmenu.proxy import *
from pymt.ui.window.win_glut import MTWindowGlut
from mtmenu.models import ApplicationProxy, CategoryProxy
from mtmenu.utils import *
from mtmenu.ui import *
from mtmenu.ui.scatter import Scatter
from mtmenu.ui.ordermenu import OrderMenu
from mtmenu.ui.imagebutton import ImageButton
from mtmenu.ui.scatterimage import ScatterImage
from mtmenu.settings import TOP_BAR_Y, SCATTER_SIZE



if __name__ == '__main__':
    # Start TUIO proxy
    proxy.start()

    apps_grid.add( get_all_applications() )
    category_grid.add( get_all_categories() )
    
    
    # Top left logo
    logo = Scatter(size=(350,68), pos= (40, TOP_BAR_Y))
    logo.add_widget( ScatterImage(filename= 'images/logo.png', scale= 0.5) ) #icon
    logo.add_widget( MTLabel(label='SenseWall', pos= (60, 14), font_size= 40) ) #main_label
    logo.add_widget( MTLabel(label='http://sensewall.dei.uc.pt', pos= (60, 0), font_size= 16) ) #other label
    scatter.add_widget( logo )

    # Top right help icon
    help = Scatter(size=(62,62), pos= (SCATTER_SIZE[0]-68, TOP_BAR_Y))
    help.add_widget( ImageButton(filename= 'images/help.png', scale= 0.9) )
    scatter.add_widget( help )
    
    # Order by menu
    order = OrderMenu(pos= (SCATTER_SIZE[0]-250, TOP_BAR_Y)  )
    scatter.add_widget( order )
    
    # Add widgets to Scatter
    scatter.add_widget(apps_grid)
    scatter.add_widget(category_grid)


    # Add background image to MainWindow
    main_window.add_widget( ScatterImage(filename= 'images/wallpaper.jpg') )
    
    # Add Scatter to MainWindow
    main_window.add_widget(scatter)
    
    #Add gesture recognition
    main_window.add_widget(GestureScan())

    
    # Execute main loop
    runTouchApp()
