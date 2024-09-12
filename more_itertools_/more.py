from itertools import islice
from functools import partial
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
print(chunked_("ABCDW",3,strict=True))