from itertools import islice, chain ,repeat
from functools import partial
from more_itertools import chunked
from collections.abc import Sequence
from collections import deque

list_ = [1,2,3,4,5,6,7]

def take(iterable, n):
    return list(islice(iterable, n))

def raise_(exceptions,*args):
    raise exceptions(*args)


def chunked_(iterable, n, strict=False):
    iterator = iter(partial(take,iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError("n cant be None if strict is True")
        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError("iterator is not dvisible by n")
                yield chunk
        return iter(ret())
    else:
        return list(iterator)

# print(list(chunked(list_,4,strict=False)))
# print(chunked_("ABCDW",3,strict=True))

_marker =object()
def first(iterable,default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker:
            # formatted_exe = traceback.format_exc()
            # print("**"*50)
            # print(formatted_exe)
            # print("**"*50)
            raise ValueError('first() was called on an empty iterable') from e

    return default

# print(first([]))

def last(iterable,default=_marker):
    try:
        if isinstance(iterable,Sequence):
            return iterable[-1]
        elif hasattr(iterable,"__reversed__"):
            return next(reversed(iterable))
        else:
            return deque(iterable,maxlen=1)[-1]
        
    except (IndexError,TypeError,StopIteration) as e:
            if default is _marker:
                raise ValueError('last() was called on an empty iterable') from e
            return default
        

def nth_or_last(iterable, n, default=_marker):
    return last(islice(iterable, n+1), default)
    
    
def one(iterable,too_short=None,too_long=None):
    it = iter(iterable)
    try:
        first_value = next(it)
    except StopIteration as e:
        raise ( 
                too_short or ValueError("too few items in iterable expected 1")
               ) from e
    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg = (f"expected exactly one item in iterable, but got {first_value},{second_value} , and perhaps more.")
        raise too_long or ValueError(msg)
    return first_value


def interleave(*iterable):
    return list(chain.from_iterable(zip(*iterable)))


def repeat_each(iterable, n=2):
    return chain.from_iterable(map(repeat, iterable,repeat(n)))

# print(list(repeat_each("ABCD")))

def strictly_n(iterable,n,too_short= None, too_long=None):
    if too_short is None:
        too_short = lambda item_count: raise_(
            ValueError,
            f"Too few items in iterable got {item_count}"
        )
    if too_long is None:
        too_long = lambda item_count: raise_(
            ValueError,
            f"Too many items in iterable got {item_count}"
        )
    
    it =  iter(iterable)
    for i in range(n):
        try:
            item = next(it)
        except StopIteration:
            too_short(i)
            return 
        else:
            yield item
            
    try:
        next(it)
    except StopIteration:
        pass
    else:
        too_long(n+1)
        