"""
Get auxiliary functions from https://github.com/Dobiasd/undictify.git
undictify (c) 2018 Tobias Hermann
"""
import enum
from typing import Any, Callable, List, TypeVar, Union, _GenericAlias  # type: ignore

TypeT = TypeVar('TypeT')


def type_origin_is(the_type: Callable[..., TypeT], origin: Any) -> bool:
    assert hasattr(the_type, '__origin__')
    return the_type.__origin__ is origin  # type: ignore


def is_union_type(the_type: Callable[..., TypeT]) -> bool:
    """Return True if the type is a Union."""
    return (the_type is Union or  # type: ignore
            is_instance(the_type, _GenericAlias) and type_origin_is(the_type, Union))


def get_union_types(union_type: Callable[..., TypeT]) -> List[Callable[..., TypeT]]:
    """Return all types a Union can hold."""
    assert is_union_type(union_type)
    return union_type.__args__  # type: ignore


def is_optional_type(the_type: Callable[..., TypeT]) -> bool:
    """Return True if the type is an Optional."""
    if not is_union_type(the_type):
        return False
    union_args = get_union_types(the_type)
    return any(is_none_type(union_arg) for union_arg in union_args)


def is_enum_type(the_type: Callable[..., TypeT]) -> bool:
    """Return True if the type is an Enum."""
    try:
        return issubclass(the_type, enum.Enum)  # type: ignore
    except TypeError:
        return False


def is_union_of_builtins_type(the_type: Callable[..., TypeT]) -> bool:
    """Return True if the type is an Union only made of
    None, str, int, float and bool."""
    if not is_union_type(the_type):
        return False
    union_args = get_union_types(the_type)
    return all(map(is_builtin_type, union_args))


def is_builtin_type(the_type: Callable[..., TypeT]) -> bool:
    """Return True if the type is a NoneType, str, int, float or bool."""
    return the_type in [str, int, bool, float, type(None)]  # type: ignore


def is_none_type(value: TypeT) -> bool:
    """Return True if the value is of NoneType."""
    return value is type(None)


def is_dict(value: TypeT) -> bool:
    """Return True if the value is a dictionary."""
    return isinstance(value, dict)


def is_list(value: TypeT) -> bool:
    """Return True if the value is a list."""
    return isinstance(value, list)


def is_instance(value: TypeT, the_type: Callable[..., TypeT]) -> bool:
    return isinstance(value, the_type)  # type: ignore
