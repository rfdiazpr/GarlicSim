# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `NavigationPanel` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil

import wx
import wx.lib.dialogs
import pkg_resources

from garlicsim.general_misc.comparison_tools import underscore_hating_key
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx

from . import images as __images_package
images_package = __images_package.__name__

# blocktodo: Back and forward buttons should be grayed out sometimes.

class NavigationPanel(wx.Panel):
    '''
    Panel for navigating between simpacks.
    
    It contains a filter/search box, back and forward buttons, and an "Add\
    simpacks from a different folder" button.
    '''
    def __init__(self, simpack_selection_dialog):
        wx.Panel.__init__(
            self,
            simpack_selection_dialog,
        )
        
        self.simpack_selection_dialog = simpack_selection_dialog
        assert isinstance(self.simpack_selection_dialog,
                          SimpackSelectionDialog)
        
        self.SetBackgroundColour(
            self.simpack_selection_dialog.GetBackgroundColour()
        )
        
        self.big_v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.big_v_sizer)
        
        self.add_simpacks_from_a_different_folder_button = wx.Button(
            self,
            label='&Add simpacks from a different folder...'
        )
        self.add_simpacks_from_a_different_folder_button.SetHelpText(
            "By default, GarlicSim lets you use simpacks that are included in "
            "GarlicSim's simpack library. If you want to use a different "
            "simpack, press this button and choose the folder that *contains* "
            "your simpack."
        )
        self.big_v_sizer.Add(
            self.add_simpacks_from_a_different_folder_button,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        self.Bind(wx.EVT_BUTTON,
                  self.simpack_selection_dialog.\
                       on_add_folder_containing_simpacks_button,
                  self.add_simpacks_from_a_different_folder_button)
        
        self.small_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.big_v_sizer.Add(
            self.small_h_sizer,
            proportion=0,
            flag=wx.EXPAND
        )
        
        ### Building filter box: ##############################################
        #                                                                     #
        
        filter_help_text = ('Type text in the filter box in order to filter '
                            'the simpacks. You will see only the simpacks '
                            'that contain the text that you typed. For '
                            'example, type "Physics" in order to see only '
                            'Physics-related simpacks.')
        self.filter_sizer = wx.BoxSizer(wx.VERTICAL)
        self.small_h_sizer.Add(
            self.filter_sizer,
            proportion=1,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=5
        )
        
        self.filter_static_text = wx.StaticText(
            self,
            label='&Filter simpacks:'
        )
        self.filter_static_text.SetHelpText(filter_help_text)
        self.filter_sizer.Add(
            self.filter_static_text,
            proportion=1,
            flag=wx.ALIGN_LEFT | wx.TOP,
            border=5,
        )
            
        
        # blocktodo: if `wx.SearchCtrl` doesn't give us everything we need, can
        # find something else.
        # blocktodo: not getting enough padding for the search control on Mac
        self.search_ctrl = wx.SearchCtrl(self)
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetDescriptiveText('')
        self.search_ctrl.SetHelpText(filter_help_text)
        self.filter_sizer.Add(
            self.search_ctrl,
            proportion=0,
            flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
            border=5,
        )
        #                                                                     #
        ### Finished building filter box. #####################################
        
        ### Building back and forward buttons: ################################
        #                                                                     #
        
        # Two peculiar things about how we're binding events here, both due to
        # accelerator weirdnesses:
        #  1. We're binding events to the parent instead of the current widget
        #     because otherwise accelerators don't work on parent on GTK.
        #  2. We're binding both button event *and* menu events, because on Mac
        #     accelerators can only trigger menu events.
        
        self.back_button = wx.BitmapButton(
            self,
            bitmap=wx.BitmapFromImage(
                wx.ImageFromStream(
                    pkg_resources.resource_stream(images_package,
                                                  'back.png'),
                    wx.BITMAP_TYPE_ANY
                )
            ),
        )
        self.simpack_selection_dialog.Bind(wx.EVT_BUTTON,
                                           lambda event: self.back(),
                                           source=self.back_button)
        self.simpack_selection_dialog.Bind(wx.EVT_MENU,
                                           lambda event: self.back(),
                                           source=self.back_button)
        self.back_button.SetToolTipString(
            u'Back (%s)' % wx_tools.keyboard.keys.back_key_string
        )
        self.back_button.SetHelpText(
            u'Go to the previously-selected simpack. (%s)' % 
            wx_tools.keyboard.keys.back_key_string
        )
        
        self.small_h_sizer.Add(
            self.back_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        
        self.forward_button = wx.BitmapButton(
            self,
            bitmap=wx.BitmapFromImage(
                wx.ImageFromStream(
                    pkg_resources.resource_stream(images_package,
                                                  'forward.png'),
                    wx.BITMAP_TYPE_ANY
                )
            ),
        )
        self.simpack_selection_dialog.Bind(wx.EVT_BUTTON,
                                           lambda event: self.forward(),
                                           source=self.forward_button)
        self.simpack_selection_dialog.Bind(wx.EVT_MENU,
                                           lambda event: self.forward(),
                                           source=self.forward_button)
        self.forward_button.SetToolTipString(
            u'Forward (%s)' % wx_tools.keyboard.keys.forward_key_string
        )
        self.forward_button.SetHelpText(
            u'Go to the simpack you visited before you hit the back button. '
            '(%s)' % wx_tools.keyboard.keys.forward_key_string
        )
        self.small_h_sizer.Add(
            self.forward_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        #                                                                     #
        ### Finished building back and forward buttons. #######################
        
        if wx_tools.is_mac:
            self.big_v_sizer.AddSpacer(
                MAC_BOTTOM_SPACING_SIZE
            )
        
        self.simpack_selection_dialog.add_accelerators(
            {wx_tools.keyboard.keys.back_keys: self.back_button.Id,
             wx_tools.keyboard.keys.forward_keys: self.forward_button.Id}
        )

            
    def back(self):
        '''Go to the previously-selected simpack.'''
        wx.lib.dialogs.messageDialog(self, 'Back')
    
    
    def forward(self):
        '''Go to the simpack that was selected before we hit "Back".'''
        wx.lib.dialogs.messageDialog(self, 'Forward')
    
    

from .simpack_selection_dialog import (SimpackSelectionDialog,
                                       MAC_BOTTOM_SPACING_SIZE)