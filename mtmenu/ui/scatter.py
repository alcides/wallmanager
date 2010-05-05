from pymt.ui.widgets.scatter import MTScatterWidget


class Scatter( MTScatterWidget ):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        super(Scatter, self).__init__(**kwargs)


