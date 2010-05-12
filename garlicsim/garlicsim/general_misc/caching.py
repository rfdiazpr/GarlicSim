
# todo: use this in all the places where i `get` shit in garlicsim_wx, like
# get_background_brush

import functools

def cache(function):
    # todo: kwargs support
    # todo: try to be smart and figure out the function's signature, then be
    # able to understand that squared(x) is the same as sqaured(number=x).
    if hasattr(function, 'cache'): return function
    
    def cached(*args):
        
        try:
            return cached.cache[args]
        except KeyError:
            cached.cache[args] = value = function(*args)
            return value
            
    cached.cache = {} # weakref.WeakKeyDictionary()
    # todo: no weakref on this baby, be advised
    
    functools.update_wrapper(cached, function)
    
    return cached


class CachedType(type): # tododoc: to simpack_wx_grokker too    
    @cache
    def __call__(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)