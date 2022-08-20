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


def and_associative(hpqr: And[And[P, Q], R]) -> And[P, And[Q, R]]:  # (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
    return And(
        hpqr.left.left,
        And(
            hpqr.left.right,
            hpqr.right
        )
    )


def and_distributive_a(hpqr: And[P, Or[Q, R]]) ->  Or[And[P, Q], And[P, R]]:  # p ∧ (q ∨ r) → (p ∧ q) ∨ (p ∧ r)
    return hpqr.right.eliminate(
        lambda hq: Left(And(hpqr.left, hq)),
        lambda hr: Right(And(hpqr.left, hr))
    )


def and_distributive_b(hpqpr: Or[And[P, Q], And[P, R]]) -> And[P, Or[Q, R]]:  # (p ∧ q) ∨ (p ∧ r) → p ∧ (q ∨ r)
    return hpqpr.eliminate(
        lambda hpq: And(hpq.left, Left(hpq.right)),
        lambda hpr: And(hpr.left, Right(hpr.right))
    )


def or_distributive_a(hpqr: Or[P, And[Q, R]]) -> And[Or[P, Q], Or[P, R]]:  # p ∨ (q ∧ r) → (p ∨ q) ∧ (p ∨ r)
    return hpqr.eliminate(
        lambda hp: And(Left(hp), Left(hp)),
        lambda hqr: And(Right(hqr.left), Right(hqr.right))
    )


def or_distributive_b(hpqpr: And[Or[P, Q], Or[P, R]]) -> Or[P, And[Q, R]]:  # (p ∨ q) ∧ (p ∨ r) → p ∨ (q ∧ r)
    def derive_pqr(hp: P) -> Or[P, And[Q, R]]:
        return Left(hp)
    
    return hpqpr.left.eliminate(
        lambda hp: derive_pqr(hp),
        lambda hq: hpqpr.right.eliminate(
            lambda hp: Left(hp),
            lambda hr: Right(And(hq, hr))
        )
    )
