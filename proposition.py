from typing import TypeVar, Generic
from collections.abc import Callable
from abc import ABCMeta, abstractmethod
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class Or(Generic[S, T], metaclass=ABCMeta):
    @abstractmethod
    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        ...

    @classmethod
    def intro_left(cls, left: S):
        return Left(left)

    @classmethod
    def intro_right(cls, right: T):
        return Right(right)


class Left(Or[S, T]):
    def __init__(self, left: S):
        self.left = left

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return left_case(self.left)


class Right(Or[S, T]):
    def __init__(self, right: T):
        self.right = right

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return right_case(self.right)


class And(Generic[S, T]):
    def __init__(self, left: S, right: T):
        self.left = left
        self.right = right

    @classmethod
    def intro(cls, left: S, right: T):
        return cls(left, right)


class Implies(Generic[S, T]):
    def __init__(self, mapping: Callable[[S], T]):
        self.mapping = mapping

    def apply(self, domain: S) -> T:
        return self.mapping(domain)


class Bottom:
    pass


class Not(Generic[S], Implies[S, Bottom]):
    pass


class P:
    pass


class Q:
    pass


class R:
    pass


def or_commutative(hpq: Or[P, Q]) -> Or[Q, P]:  # P ∨ Q → Q ∨ P
    return hpq.eliminate(
        lambda hp: Right(hp),
        lambda hq: Left(hq)
    )


def and_commutative(hpq: And[P, Q]) -> And[Q, P]:  # P ∧ Q → Q ∧ P
    return And(hpq.right, hpq.left)


def or_associative(hpqr: Or[Or[P, Q], R]) -> Or[P, Or[Q, R]]:  # (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
    def derive_qr_from_q(hq: Q) -> Or[Q, R]:
        return Left(hq)

    def derive_qr_from_r(hr: R) -> Or[Q, R]:
        return Right(hr)

    return hpqr.eliminate(
        lambda hpq: hpq.eliminate(
            lambda hp: Left(hp),
            lambda hq: Right(derive_qr_from_q(hq))
        ),
        lambda hr: Right(derive_qr_from_r(hr))
    )


def and_associative(hpqr: And[And[P, Q], R]) -> And[P, And[Q, R]]: # (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
    return And(
        hpqr.left.left,
        And(hpqr.left.right, hpqr.right)
    )
