from __future__ import annotations
from typing import Callable, Any, Generic, NoReturn, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Some(Generic[T]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: T

    def __init__(self, value: T = None):
        self.value = value

    def bind(self, func: Callable[[T], Option[U]]) -> Option[U]:
        return func(self.value)

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return Some(func(self.value))

    def get(self) -> T:
        return self.value


class Nothing:
    def __init__(self):
        pass

    def bind(self, _: Callable[[Any], Option[Any]]) -> Nothing:
        return self

    def map(self, _: Callable[[Any], Any]) -> Nothing:
        return self

    def get(self) -> NoReturn:
        raise ValueError


Option = Some[T] | Nothing
