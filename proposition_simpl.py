from typing import Tuple


class P:
    pass


class Q:
    pass


class R:
    pass


# P ∨ Q → Q ∨ P
def or_commutative(hpq: P | Q) -> Q | P:
    return hpq


# P ∧ Q → Q ∧ P
def and_commutative(hpq: Tuple[P, Q]) -> Tuple[Q, P]:
    return hpq[1], hpq[0]


# (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
def or_associative(hpqr: (P | Q) | R) -> P | (Q | R):
    return hpqr


# (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
def and_associative(hpqr: Tuple[Tuple[P, Q], R]) -> Tuple[P, Tuple[Q, R]]:
    return hpqr[0][0], (hpqr[0][1], hpqr[1])
