import typing

TA = typing.TypeVar("TA")
TB = typing.TypeVar("TB")
U = typing.TypeVar("U")


class Option(typing.Generic[TA]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: TA

    def __init__(self, value: TA = None):
        self.value = value

    def bind(self, func: typing.Callable[[TA], "Option[TB]"]) -> "Option[TB]":
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> "Option[TB]":
        return Some(func(self.value))

    def get(self) -> TA:
        return self.value


class Some(Option[TA]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: TA

    def __init__(self, value: TA = None):
        self.value = value

    def bind(self, func: typing.Callable[[TA], Option[TB]]) -> Option[TB]:
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> Option[TB]:
        return Some(func(self.value))

    def get(self) -> TA:
        return self.value


class Nothing(Option[TA]):
    def __init__(self):
        pass

    def bind(self, _: typing.Callable[..., Option[TA]]) -> Option[TA]:
        return self

    def map(self, _: typing.Callable[..., TA]) -> Option[TA]:
        return self

    def get(self) -> typing.NoReturn:
        raise ValueError
