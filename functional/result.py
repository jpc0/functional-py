import typing

T = typing.TypeVar("T")
U = typing.TypeVar("U")


class Result(typing.Protocol, typing.Generic[T, U]):
    def __init__(self, value: T):
        ...

    def bind(self, func: typing.Callable[[T], "Result[T, U]"]) -> "Result[T, U]":
        ...

    def map(self, func: typing.Callable[[T], U]) -> "Result[T, U]":
        ...

    def get(self) -> T:
        ...


class Ok(Result[T, U]):
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

    def bind(self, func: typing.Callable[[T], Result[T, U]]) -> Result[T, U]:
        return func(self.value)

    def map(self, func: typing.Callable[[T], U]) -> Result[T, U]:
        return Ok(func(self.value))

    def get(self) -> T:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


class Err(Result[T, U]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: U

    def __init__(self, value: U):
        if isinstance(value, Ok | Err):
            self.value = value.value
        else:
            self.value = value

    def bind(self, _: typing.Callable[..., Result[T, U]]) -> Result[T, U]:
        return self

    def map(self, _: typing.Callable[..., U]) -> Result[T, U]:
        return self

    def get(self) -> U:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"
