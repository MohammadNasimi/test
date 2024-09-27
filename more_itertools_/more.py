from itertools import islice
from functools import partial
import traceback
from more_itertools import chunked

list_ = [1,2,3,4,5,6,7]

def take(iterable, n):
    return list(islice(iterable, n))

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