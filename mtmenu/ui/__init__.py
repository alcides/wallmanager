from ui.mainwindow import MainWindow
main_window = MainWindow()

# APPSLIST
from mtmenu.ui.appslist import AppsList
from utils import get_all_applications
apps_list = AppsList(get_all_applications())

# TOPBAR
from ui.topbar import TopBar
top_bar = TopBar()

# CATEGORIES LIST
from ui.categorylist import CategoryList
from utils import get_all_categories
categories_list = CategoryList(apps_list, get_all_categories())

# PROXY
from proxy import Proxy
proxy = Proxy()

# BACKGROUND
from ui.backgroundimage import BackgroundImage
background_image = BackgroundImage(filename = 'images/wallpaper.png')

# COVERWINDOW
from ui.coverwindow import CoverWindow
cover_window = CoverWindow()