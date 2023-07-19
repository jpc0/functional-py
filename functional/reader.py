from __future__ import annotations
from typing import Callable, Generic, TypeVar

TA = TypeVar("TA")
TB = TypeVar("TB")
U = TypeVar("U")


class Reader(Generic[U, TA]):
    __slots__ = "func"

    func: Callable[[U], TA]

    def __init__(self, func: Callable[[U], TA]):
        self.func = func

    def run(self, env: U):
        return self.func(env)

    def map(self, func: Callable[[TA], TB]) -> Reader[U, TB]:
        def new_action(env: U):
            x = self.run(env)
            return func(x)

        return Reader(new_action)

    @staticmethod
    def retn(x: TA) -> Reader[U, TA]:
        def new_action(_: U):
            return x

        return Reader(new_action)

    def apply(self, func_action: Reader[U, Callable[[TA], TB]]) -> Reader[U, TB]:
        def new_action(env: U):
            f = func_action.run(env)
            x = self.run(env)
            return f(x)

        return Reader(new_action)

    def bind(self, func: Callable[[TA], Reader[U, TB]]) -> Reader[U, TB]:
        def new_action(env: U):
            x = self.run(env)
            return func(x).run(env)

        return Reader(new_action)
