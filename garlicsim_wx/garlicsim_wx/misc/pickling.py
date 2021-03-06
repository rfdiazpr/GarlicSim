# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `Pickler` and `Unpickler` classes.

See their documentation for more details.
'''

from garlicsim.general_misc import pickle_tools


class Pickler(pickle_tools.CutePickler):
    '''Pickler for pickling a `GuiProject`.'''
    def __init__(self, file_, protocol=2): 
        pickle_tools.CutePickler.__init__(self, file_, protocol)

    def pre_filter(self, thing):
        return (getattr(thing, '__module__', None) != '__garlicsim_shell__')

    
class Unpickler(pickle_tools.CuteUnpickler):
    '''Unpickler for unpickling a `GuiProject`.'''

