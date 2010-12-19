# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `BaseStepType` class.

See its documentation for more details.
'''

# todo: should this be a metaclass?
# todo: does this mixed abc enforce anything, with our custom `__call__`?

import types

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import logic_tools
from garlicsim.general_misc import caching


class StepType(abc.ABCMeta):

    def __call__(cls, step_function):
        step_function._BaseStepType__step_type = cls
        return step_function

    
    def __instancecheck__(cls, thing):
        
        step_type = StepType.get_step_type(thing)
        if step_type:
            return issubclass(step_type, cls)
        else:
            assert step_type is None
            return False
        
    
    @staticmethod
    def get_step_type(thing):
        
        if hasattr(thing, '_BaseStepType__step_type'):
            return thing._BaseStepType__step_type
        
        if not callable(thing) or not hasattr(thing, '__name__'):
            return None
        
        step_types = BaseStep.__subclasses__()
        
        all_name_identifiers = [cls_.name_identifier for cls_ in step_types]        
                
        matching_name_identifiers = \
            [name_identifier for name_identifier in all_name_identifiers if
             name_identifier in thing.__name__]
        
        if not matching_name_identifiers:
            step_type = None
                    
        else:
            (maximal_matching_name_identifier,) = logic_tools.logic_max(
                matching_name_identifiers,
                relation=str.__contains__
            )
            
            (step_type,) = \
                [step_type for step_type in step_types if
                 step_type.name_identifier == maximal_matching_name_identifier]
        
            
        actual_function = (
            thing.im_func if
            isinstance(thing, types.MethodType)
            else thing
        )
        actual_function._BaseStepType__step_type = step_type
            
        return step_type
        
                
class BaseStep(object):
    '''
    A type of step function.
    
    There are several different types of step functions with different
    advantages and disadvantages. See the
    `garlicsim.misc.simpack_grokker.step_types` package for a collection of
    various step types.
    '''
    __metaclass__ = StepType


    name_identifier = abc.abstractproperty()
    
    
    verbose_name = abc.abstractproperty()
    '''The verbose name of the step type.'''

    
    step_iterator_class = abc.abstractproperty()
    '''The step iterator class used for steps of this step type.'''    
    
    