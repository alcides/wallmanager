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
categories_list = CategoryList(get_all_categories())

# PROXY
from proxy import Proxy
proxy = Proxy()

# BACKGROUND
from ui.backgroundimage import BackgroundImage
background_image = BackgroundImage(filename = 'images/wallpaper.png')

# PROJECTORS CHECKER
from projectors_interface import ActivityChecker 
activity_checker = ActivityChecker()


# COVERWINDOW
from ui.coverwindow import CoverWindow
from gesture.gesture_scan import GestureScan
cover_window = CoverWindow()
cover_window.add_widget(GestureScan(activity_checker))


# SELF HANDLE
import win32gui
self_hwnd = win32gui.GetForegroundWindow()



