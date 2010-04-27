from pymt import *
from pymt.input.postproc.doubletap import InputPostprocDoubleTap

class AppButton(MTKineticItem):
    """Widget representing an application on main window. 
    
    Arguments:
        app -- Application object attached to this widget
        kwargs -- Button properties, most of them inherited from MTButton
    
    This widget should be added to AppsGrid on Menu's UI construction"""
    def __init__(self, app, **kwargs):
        kwargs.setdefault('label', unicode(app))
        kwargs.setdefault('deletable', False)
        kwargs.setdefault('anchor_x', 'center')
        kwargs.setdefault('anchor_y', 'middle')
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('size', (200,200))        
        
        self.app = app
        super(AppButton, self).__init__(**kwargs)


    """Execute application on click"""
    def on_press( self, touch ):
        if touch.is_double_tap:
            self.handle_double_tap()
        else:
            return
        
        
    def handle_double_tap(self):
        print '\nLoading %s...\n' % unicode(self.app)
        print 'ID: %i' % self.app.id
        print '\tPath: %s\n' % self.app.get_extraction_fullpath
        print '\tBoot file: %s\n' % self.app.get_boot_file()
        self.app.execute()

