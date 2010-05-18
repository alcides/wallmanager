from pymt.ui.widgets.scatter import MTScatterImage


class ScatterImage( MTScatterImage ):
    
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (1000,1000))
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('auto_bring_to_front', False)
        super(ScatterImage, self).__init__(**kwargs)

