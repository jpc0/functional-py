from __future__ import annotations
from typing import Callable, Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Ok(Generic[T]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: T

    def __init__(self, value: T):
        if isinstance(value, Ok):
            self.value = value.value
        elif isinstance(value, Err):
            raise Exception("Cannot convert Err to Ok")
        else:
            self.value = value

    def bind(self, func: Callable[[Any], Result[T, U]]) -> Result[T, U]:
        return func(self.value)

    def map(self, func: Callable[[T], Any]) -> Ok[T]:
        return Ok(func(self.value))

    def get(self) -> T:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


class Err(Generic[U]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: U

    def __init__(self, value: U):
        if isinstance(value, Ok | Err):
            self.value = value.value
        else:
            self.value = value

    def bind(self, _: Callable[[Any], Result]) -> Err[U]:
        return self

    def map(self, _: Callable[[Any], Any]) -> Err[U]:
        return self

    def get(self) -> U:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


Result = Ok[T] | Err[U]
