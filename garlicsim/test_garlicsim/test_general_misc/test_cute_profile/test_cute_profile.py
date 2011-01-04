# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.cute_profile`.
'''

from garlicsim.general_misc import cute_profile
from garlicsim.general_misc import cute_inspect

from .shared import call_and_check_if_profiled


def func(x, y, z=3):
    '''Function that does some meaningless number-juggling.'''
    sum([1, 2, 3])
    set([1, 2]) | set([2, 3])
    return x, y, z



def test_simple():
    '''Test the basic workings of `profile_ready`.'''
    f = cute_profile.profile_ready()(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    f = cute_profile.profile_ready(condition=True)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    f = cute_profile.profile_ready(condition=True, off_after=False)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    
    
    f = cute_profile.profile_ready(off_after=True)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.condition = lambda f, *args, **kwargs: True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    
def test_method():
    '''Test that `profile_ready` works as a method decorator.'''
    
    class A(object):
        def __init__(self):
            self.x = 0
                
        @cute_profile.profile_ready(off_after=False)
        def increment(self):
            sum([1, 2, 3])
            self.x += 1
            
    a = A()
    assert a.x == 0
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 1
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 2
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 3

    a.increment.im_func.profiling_on = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 4
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 5
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 6
    
    a.increment.im_func.off_after = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 7
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 8
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 9
    
    a.increment.im_func.profiling_on = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 10
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 11
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 12
    
    

def test_condition():
    '''Test the `condition` argument of `profile_ready`.'''

    x = 7
    
    @cute_profile.profile_ready(condition=lambda function, y: x == y,
                                off_after=False)
    def f(y):
        pass
    
    # Condition is `False`:
    assert call_and_check_if_profiled(lambda: f(5)) is False
    assert call_and_check_if_profiled(lambda: f(6)) is False
    
    # Condition is `True`:
    assert call_and_check_if_profiled(lambda: f(7)) is True
    
    # So now profiling is on regardless of condition:
    assert call_and_check_if_profiled(lambda: f(8)) is True
    assert call_and_check_if_profiled(lambda: f(9)) is True
    assert call_and_check_if_profiled(lambda: f(4)) is True
    assert call_and_check_if_profiled(lambda: f('frr')) is True
    
    # Setting profiling off:
    f.profiling_on = False
        
    # So no profiling now:
    assert call_and_check_if_profiled(lambda: f(4)) is False
    assert call_and_check_if_profiled(lambda: f('frr')) is False
    
    # Until the condition becomes `True` again: (And this time, for fun, with a
    # different `x`:)
    x = 9
    assert call_and_check_if_profiled(lambda: f(9)) is True
    
    # So now, again, profiling is on regardless of condition:
    assert call_and_check_if_profiled(lambda: f(4)) is True
    assert call_and_check_if_profiled(lambda: f('frr')) is True
    
    # Let's give it a try with `.off_after = True`:
    f.off_after = True
    
    # Setting profiling off again:
    f.profiling_on = False
    
    # And for fun set a different `x`:
    x = 'wow'
    
    # Now profiling is on only when the condition is fulfilled, and doesn't
    # stay on after:
    assert call_and_check_if_profiled(lambda: f('ooga')) is False
    assert call_and_check_if_profiled(lambda: f('booga')) is False
    assert call_and_check_if_profiled(lambda: f('wow')) is True
    assert call_and_check_if_profiled(lambda: f('meow')) is False
    assert call_and_check_if_profiled(lambda: f('kabloom')) is False
    
    # In fact, after successful profiling the condition gets reset to `None`:
    assert f.condition is None
    
    # So now if we'll call the function again, even if the (former) condition
    # is `True`, there will be no profiling:
    assert call_and_check_if_profiled(lambda: f(9)) is False
    
    # So if we want to use a condition again, we have to set it ourselves:
    f.condition = lambda f, y: isinstance(y, float)
    
    # And again (since `.off_after == True`) profiling will turn on for just
    # one time when the condition evaluates to `True` :
    assert call_and_check_if_profiled(lambda: f('kabloom')) is False
    assert call_and_check_if_profiled(lambda: f(3)) is False
    assert call_and_check_if_profiled(lambda: f(3.1)) is True
    assert call_and_check_if_profiled(lambda: f(3.1)) is False
    assert call_and_check_if_profiled(lambda: f(-4.9)) is False
    
    
def test_signature_perservation():
    '''Test that the `profile_ready` decorator preserves function signature.'''
    assert cute_inspect.getargspec(func) == \
           cute_inspect.getargspec(cute_profile.profile_ready()(func))