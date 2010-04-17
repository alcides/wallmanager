from pymt import *


class AppButton(MTKineticItem):
    """Widget representing an application on main window. 
    
    Arguments:
        app -- Application object attached to this widget
        kwargs -- Button properties, most of them inherited from MTButton
    
    This widget should be added to AppsGrid on Menu's UI construction"""
    def __init__(self, app, **kwargs):
        self.app = app

        kwargs.setdefault('label', unicode(app))
        kwargs.setdefault('deletable', False)
        #kwargs.setdefault('width', 90)
        #kwargs.setdefault('height', 40)
        #kwargs.setdefault('font_size', 16)
        super(AppButton, self).__init__(**kwargs)

    """Execute application on click"""
    def on_press( self, touch ):
        print '\nLoading %s...' % unicode(self.app)
        print 'ID: %i' % self.app.id
        print 'Path: %s' % self.app.get_extraction_fullpath()
        print 'Boot file: %s' % self.app.get_boot_file()
        self.app.execute()