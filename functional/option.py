import typing

T = typing.TypeVar("T")
U = typing.TypeVar("U")


class Option(typing.Generic[T]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: T

    def __init__(self, value: T = None):
        self.value = value

    def bind(self, func: typing.Callable[[T], "Option[U]"]) -> "Option[U]":
        return func(self.value)

    def map(self, func: typing.Callable[[T], U]) -> "Option[U]":
        return Some(func(self.value))

    def get(self) -> T:
        return self.value


class Some(Option[T]):
    __match_args__ = ("value",)
    __slots__ = "value"

    value: T

    def __init__(self, value: T = None):
        self.value = value

    def bind(self, func: typing.Callable[[T], Option[U]]) -> Option[U]:
        return func(self.value)

    def map(self, func: typing.Callable[[T], U]) -> Option[U]:
        return Some(func(self.value))

    def get(self) -> T:
        return self.value


class Nothing(Option[T]):
    def __init__(self):
        pass

    def bind(self, _: typing.Callable[..., Option[T]]) -> Option[T]:
        return self

    def map(self, _: typing.Callable[..., T]) -> Option[T]:
        return self

    def get(self) -> typing.NoReturn:
        raise ValueError
