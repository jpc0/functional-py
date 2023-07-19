import typing

TA = typing.TypeVar("TA")
TB = typing.TypeVar("TB")
U = typing.TypeVar("U")


class ResultT(typing.Protocol, typing.Generic[TA, U]):
    def __init__(self, value: TA):
        ...

    def bind(self, func: typing.Callable[[TA], "ResultT[TB, U]"]) -> "ResultT[TB, U]":
        ...

    def map(self, func: typing.Callable[[TA], TB]) -> "ResultT[TB, U]":
        ...

    def get(self) -> TA:
        ...

    def apply(self, func: "ResultT[typing.Callable[[TA], TB], U]") -> "ResultT[TB, U]":
        ...


class Ok(ResultT[TA, U]):
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

    def bind(self, func: typing.Callable[[TA], ResultT[TB, U]]) -> ResultT[TB, U]:
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> ResultT[TB, U]:
        return Ok(func(self.value))

    def get(self) -> TA:
        return self.value

    def apply(self, func: "ResultT[typing.Callable[[TA], TB], U]") -> "ResultT[TB, U]":
        return Ok(func.get()(self.value))

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


class Err(ResultT[TA, U]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: U

    def __init__(self, value: U):
        if isinstance(value, Ok | Err):
            self.value = value.value
        else:
            self.value = value

    def bind(self, _: typing.Callable[..., ResultT[TA, U]]) -> ResultT[TA, U]:
        return self

    def map(self, _: typing.Callable[..., TA]) -> ResultT[TA, U]:
        return self

    def get(self) -> U:
        return self.value

    def apply(self, _: "ResultT[typing.Callable[..., TA], U]") -> "ResultT[TA, U]":
        return self

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


Result = Ok[TA, U] | Err[TA, U]
