from typing import TypeVar, Tuple


class P:
    pass


class Q:
    pass


class R:
    pass


def or_commutative(hpq: P | Q) -> Q | P:  # P ∨ Q → Q ∨ P
    return hpq


def and_commutative(hpq: Tuple[P, Q]) -> Tuple[Q, P]:  # P ∧ Q → Q ∧ P
    return hpq[1], hpq[0]


def or_associative(hpqr: (P | Q) | R) -> P | (Q | R):  # (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
    return hpqr


def and_associative(hpqr: Tuple[Tuple[P, Q], R]) -> Tuple[P, Tuple[Q, R]]:  # (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
    return hpqr[0][0], (hpqr[0][1], hpqr[1])


