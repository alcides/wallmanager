from pymt.ui.widgets.composed.popup import MTPopup


class Popup( MTPopup ):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'MTPopup')
        kwargs.setdefault('size', (215,160))
        kwargs.setdefault('pos', (20,20))
        kwargs.setdefault('label_submit', 'Yes')
        kwargs.setdefault('label_cancel', 'No')
        kwargs.setdefault('show_cancel', True)
        kwargs.setdefault('exit_on_submit', True)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_scale', False) 

        super(Popup, self).__init__(**kwargs)