import typing

TA = typing.TypeVar("TA")
TB = typing.TypeVar("TB")
U = typing.TypeVar("U")


class Result(typing.Protocol, typing.Generic[TA, U]):
    def __init__(self, value: TA):
        ...

    def bind(self, func: typing.Callable[[TA], "Result[TB, U]"]) -> "Result[TB, U]":
        ...

    def map(self, func: typing.Callable[[TA], TB]) -> "Result[TB, U]":
        ...

    def get(self) -> TA:
        ...


class Ok(Result[TA, U]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: TA

    def __init__(self, value: TA):
        if isinstance(value, Ok):
            self.value = value.value
        elif isinstance(value, Err):
            raise Exception("Cannot convert Err to Ok")
        else:
            self.value = value

    def bind(self, func: typing.Callable[[TA], Result[TB, U]]) -> Result[TB, U]:
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> Result[TB, U]:
        return Ok(func(self.value))

    def get(self) -> TA:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


class Err(Result[TA, U]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: U

    def __init__(self, value: U):
        if isinstance(value, Ok | Err):
            self.value = value.value
        else:
            self.value = value

    def bind(self, _: typing.Callable[..., Result[TA, U]]) -> Result[TA, U]:
        return self

    def map(self, _: typing.Callable[..., TA]) -> Result[TA, U]:
        return self

    def get(self) -> U:
        return self.value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"
