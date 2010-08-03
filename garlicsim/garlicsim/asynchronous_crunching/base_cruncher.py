# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the BaseCruncher class.

See its documentation for more information. See the `crunchers` package for a
collection of crunchers.
'''

import copy

from garlicsim.general_misc.third_party import abc


class BaseCruncher(object):
    '''
    A cruncher receives a state from the main program, and then it repeatedly
    applies the step function of the simulation to produce more states. Those
    states are then put in the cruncher's `work_queue`. They are then taken by
    the main program when `Project.sync_crunchers` is called, and put into the
    tree.

    The cruncher also receives a crunching profile from the main program. The
    crunching profile specifes how far the cruncher should crunch the
    simulation, and which arguments it should pass to the step function.
    
    This package may define different crunchers which work in different ways,
    but are to a certain extent interchangable. Different kinds of crunchers
    have different advantages and disadvantges relatively to each other, and
    which cruncher you should use for your project depends on the situation.
    '''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        self.crunching_manager = crunching_manager
        self.project = crunching_manager.project
        self.initial_state = initial_state
        self.crunching_profile = copy.deepcopy(crunching_profile)
    
        
    @abc.abstractmethod
    def retire(self):
        '''Retire the cruncher, making it shut down.'''
        pass
    
    
    @abc.abstractmethod
    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile.'''
        self.order_queue.put(profile)
        
    
    @abc.abstractmethod
    def is_alive(self):
        '''Report whether the cruncher is alive and crunching.'''