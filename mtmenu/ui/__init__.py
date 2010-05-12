from mtmenu.settings import APPS_GRID_POSITION, APPS_GRID_SIZE, CATEGORY_GRID_POSITION, CATEGORY_GRID_SIZE
from mtmenu.gesture.gesture_scan import GestureScan


from ui.mainwindow import MainWindow
main_window = MainWindow(width=800, height=600)


from ui.coverwindow import CoverWindow
cover_window = CoverWindow()
#Add gesture recognition
cover_window.add_widget(GestureScan())

# Scatter to make AppsList movable
from mtmenu.ui.mainscatter import MainScatter
scatter = MainScatter()


# Construct AppsList looping through all apps
from mtmenu.ui.appslist import AppsList
apps_grid = AppsList(pos= APPS_GRID_POSITION, size= APPS_GRID_SIZE)
 
 
# Construct CategoryList looping through all categories 
from mtmenu.ui.categorylist import CategoryList
category_grid = CategoryList(pos= CATEGORY_GRID_POSITION, size= CATEGORY_GRID_SIZE, style={'scrollbar-size':0}) 

