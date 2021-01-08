from typing import Dict, Type, Callable, Any, Tuple

from util import qualname, declaring_class

_ALL_VISITORS: Dict[Tuple[str, Type], Callable[[Any, Any], Any]] = {}


def _visitor_impl(self, obj):
    return _ALL_VISITORS[qualname(type(self)), type(obj)](self, obj)


# https://stackoverflow.com/a/28398903/3084276
def visitor(arg_type: Type):
    def decorator(fn: Callable[[Any, Any], Any]):
        declaring_type = declaring_class(fn)
        _ALL_VISITORS[declaring_type, arg_type] = fn
        return _visitor_impl

    return decorator
