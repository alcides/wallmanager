from settings import APPS_GRID_POSITION, APPS_GRID_SIZE, CATEGORY_GRID_POSITION, CATEGORY_GRID_SIZE


# Scatter to make AppsList movable
from scatter import Scatter
scatter = Scatter()


# Construct AppsList looping through all apps
from appslist import AppsList
apps_grid = AppsList(pos= APPS_GRID_POSITION, size= APPS_GRID_SIZE)
 
# Construct CategoryList looping through all categories 
from categorylist import CategoryList
category_grid = CategoryList(pos= CATEGORY_GRID_POSITION, size= CATEGORY_GRID_SIZE) 

