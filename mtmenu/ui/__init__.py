from settings import APPS_GRID_POSITION, APPS_GRID_SIZE, CATEGORY_GRID_POSITION, CATEGORY_GRID_SIZE


# Main Window
from mtmenu.ui.mainwindow import MainWindow
main_window = MainWindow(width=800, height=600)


from mtmenu.ui.coverwindow import CoverWindow
cover_window = CoverWindow()


# Scatter to make AppsList movable
from mtmenu.ui.scatter import Scatter
scatter = Scatter()


# Construct AppsList looping through all apps
from mtmenu.ui.appslist import AppsList
apps_grid = AppsList(pos= APPS_GRID_POSITION, size= APPS_GRID_SIZE)
 
# Construct CategoryList looping through all categories 
from mtmenu.ui.categorylist import CategoryList
category_grid = CategoryList(pos= CATEGORY_GRID_POSITION, size= CATEGORY_GRID_SIZE) 
<<<<<<< HEAD:mtmenu/ui/__init__.py

=======
>>>>>>> d6119fe... Top left logo.:mtmenu/ui/__init__.py

