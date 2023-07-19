import typing

TA = typing.TypeVar("TA")
TB = typing.TypeVar("TB")
U = typing.TypeVar("U")


class OptionT(typing.Generic[TA]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: TA

    def __init__(self, value: TA = None):
        self.value = value

    def bind(self, func: typing.Callable[[TA], "OptionT[TB]"]) -> "OptionT[TB]":
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> "OptionT[TB]":
        return Some(func(self.value))

    def get(self) -> TA:
        return self.value


class Some(OptionT[TA]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: TA

    def __init__(self, value: TA = None):
        self.value = value

    def bind(self, func: typing.Callable[[TA], OptionT[TB]]) -> OptionT[TB]:
        return func(self.value)

    def map(self, func: typing.Callable[[TA], TB]) -> OptionT[TB]:
        return Some(func(self.value))

    def get(self) -> TA:
        return self.value


class Nothing(OptionT[TA]):
    def __init__(self):
        pass

    def bind(self, _: typing.Callable[..., OptionT[TA]]) -> OptionT[TA]:
        return self

    def map(self, _: typing.Callable[..., TA]) -> OptionT[TA]:
        return self

    def get(self) -> typing.NoReturn:
        raise ValueError

Option = Some[TA] | Nothing[TA]
