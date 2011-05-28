# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CuteDialogType` metaclass.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc.wx_tools.cursors import CursorChanger
from garlicsim.general_misc import context_managers


class CuteDialogType(type):
    def __call__(self, parent, *args, **kwargs):
        context_manager = \
            CursorChanger(parent, wx.CURSOR_WAIT) if parent else \
            context_managers.BlankContextManager()
        with context_manager:
            return type.__call__(self, parent, *args, **kwargs)