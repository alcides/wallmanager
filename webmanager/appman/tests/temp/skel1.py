# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the WTFPL, Version 2, as
# published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.



# pyMT_skel1 is a simple example to get you started with multitouch
# development in python.
# In this example we will see how to use multitouch widgets that
# come pre-packaged with pyMT.

# pyMT is a multitouch framework for python. It's meant as an easy way for
# beginners to start developing multitouch applications and also to allow
# rapid prototyping of more complex software.
#
# Before starting you must install:
#     - Python 2.6 (http://www.python.org)
#     - numpy latest version (http://sourceforge.net/projects/numpy/files/)
#     - Pyglet 1.1.2 (http://www.pyglet.org)
#     - pyMT 0.3 (http://pymt.txzone.net)

# pyMT is built on top of the pyglet game creation framework, so beyond
# the API provided by pyMT itself you have access to all of the libraries
# provided by pyglet (and any extra python modules you may have installed).
#
# The necessary documentation can be found at:
#     - http://pymt.txzone.net/pages/Documentation
#     - http://pyglet.org/documentation.html



import random
import sys

from pymt import *



class Button( MTButton ):

    def __init__( self, **args ):
        args.setdefault('label', 'Exit')
        args.setdefault('width', 90)
        args.setdefault('height', 40)
        args.setdefault('font_size', 16)
        super(Button, self).__init__(**args)

    def on_press( self, touch ):
        sys.exit(0)

def main():
    """
    This is the entry point to our application. Here we setup the main
    window and everything else we need, like adding widgets to the window.

    After everything is ready, we call runTouchApp(), which starts pyMT's
    main cycle.
    """

    #This creates an OpenGL window with multitouch input capabilities.
    window = MTWindow(fullscreen=True)

    #Let's add some widgets to the window :)
    for i in range(10):
        #Calculate initial position of each widget at random
        x = random.randrange(0, window.width)
        y = random.randrange(0, window.height)

        #Random initial rotation
        rot = random.randrange(0, 360)

        #Random initial size (scale), between 0.5 and 3 times the size
        scale = random.random()*2.5 + 0.5

        scatter_image = MTScatterImage(filename='fsm.png',
                                       translation=[x,y],
                                       rotation=rot,
                                       scale=scale)
        window.add_widget(scatter_image)
        
        b=Button(translation=[0,0])
        window.add_widget(b)

    #Uncomment the next 2 lines so the mouse cursor won't appear on screen ;)
    #window.set_mouse_visible(False)
    #window.set_exclusive_mouse(True)

    #We have everything set up, so let's start the main cycle!
    runTouchApp()
    exit()



if __name__ == '__main__':
    #Check if script is being called from the command line and run main()
    main()
