from typing import Generic, TypeVar
from abc import ABCMeta, abstractmethod
from typing_extensions import Self

from proposition import Proposition


class Reflexivity(Proposition):
    pass


class Nat(metaclass=ABCMeta):
    @abstractmethod
    def __add__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def to_int(self) -> int:
        ...


M = TypeVar('M', bound=Nat)
N = TypeVar('N', bound=Nat)


class Zero(Nat):
    def __add__(self, other: Nat) -> Nat:
        return other

    def to_int(self) -> int:
        return 0


class Succ(Generic[N], Nat):
    def __init__(self, prev: Nat) -> None:
        self.prev = prev
    
    def __add__(self, other: Nat) -> Nat:
        return self.prev + Succ(other)

    def to_int(self) -> int:
        return self.prev.to_int() + 1


def to_nat(integer: int) -> Nat:
    if integer > 0:
        return Succ(to_nat(integer - 1))
    else:
        return Zero()


if __name__ == '__main__':
    print(f"Succ(Succ(Succ(Zero()))).to_int() = {Succ(Succ(Succ(Zero()))).to_int()}")
    print(f"to_nat(5).to_int() = {type(to_nat(5))}")
    print(f"(to_nat(5) + to_nat(3)).to_int() = {(to_nat(5) + to_nat(3)).to_int()}")
