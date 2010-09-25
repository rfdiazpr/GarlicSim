import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class ErrorDialog(wx.MessageDialog, CuteDialog):
    def __init__(self, parent, message, caption=''):
        wx.MessageDialog.__init__(self, parent, message, caption,
                                  wx.CANCEL | wx.ICON_ERROR)