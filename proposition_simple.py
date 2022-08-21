# These theorems are from https://leanprover.github.io/theorem_proving_in_lean4/propositions_and_proofs.html#examples-of-propositional-validities
from typing import Callable, TypeAlias, Union, Tuple, Any


Or = Union
And = Tuple
Implies = Callable
Bottom: TypeAlias = Any


# P Q R: Proposition
class P:
    pass


class Q:
    pass


class R:
    pass


# P ∨ Q → Q ∨ P
def or_commutative(hpq: Or[P, Q]) -> Or[Q, P]:
    return hpq


# P ∧ Q → Q ∧ P
def and_commutative(hpq: And[P, Q]) -> And[Q, P]:
    return (hpq[1], hpq[0])


# (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
def or_associative(hpqr: Or[Or[P, Q], R]) -> Or[P, Or[Q, R]]:
    return hpqr


# (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
def and_associative(hpqr: And[And[P, Q], R]) -> And[P, And[Q, R]]:
    return (hpqr[0][0], (hpqr[0][1], hpqr[1]))


# P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R)
def and_distributive_a(hpqr: And[P, Or[Q, R]]) -> Or[And[P, Q], And[P, R]]:
    return (hpqr[0], hpqr[1]) if isinstance(hpqr[1], Q) else (hpqr[0], hpqr[1])


# (P ∧ Q) ∨ (P ∧ R) → P ∧ (Q ∨ R)
def and_distributive_b(hpqpr: Or[And[P, Q], And[P, R]]) -> And[P, Or[Q, R]]:
    return (hpqpr[0], hpqpr[1]) if isinstance(hpqpr, (P, Q)) else (hpqpr[0], hpqpr[1])


# P ∨ (Q ∧ R) → (P ∨ Q) ∧ (P ∨ R)
def or_distributive_a(hpqr: Or[P, And[Q, R]]) -> And[Or[P, Q], Or[P, R]]:
    return (hpqr, hpqr) if isinstance(hpqr, P) else (hpqr[0], hpqr[1])


# (P ∨ Q) ∧ (P ∨ R) → P ∨ (Q ∧ R)
def or_distributive_b(hpqpr: And[Or[P, Q], Or[P, R]]) -> Or[P, And[Q, R]]:
    return hpqpr[0] if isinstance(hpqpr[0], P) else (hpqpr[1] if isinstance(hpqpr[1], P) else (hpqpr[0], hpqpr[1]))


# (P → (Q → R)) → (P ∧ Q → R)
def unify_and(hpqr: Implies[[P], Implies[[Q], R]]) -> Implies[[And[P, Q]], R]:
    return lambda hpq: hpqr(hpq[0])(hpq[1])


# (P ∧ Q → R) → (P → (Q → R))
def destruct_and(hpqr: Implies[[And[P, Q]], R]) -> Implies[[P], Implies[[Q], R]]:
    return lambda hp: lambda hq: hpqr((hp, hq))


# (P ∨ Q → R) → (P → R) ∧ (Q → R)
def destruct_or(hpqr: Implies[[Or[P, Q]], R]) -> And[Implies[[P], R], Implies[[Q], R]]:
    return (lambda hp: hpqr(hp), lambda hq: hpqr(hq))


# (P → R) ∧ (Q → R) → (P ∨ Q → R)
def unify_or(hprqr: And[Implies[[P], R], Implies[[Q], R]]) -> Implies[[Or[P, Q]], R]:
    return lambda hpq: hprqr[0](hpq) if isinstance(hpq, P) else hprqr[1](hpq)


# ¬(P ∨ Q) → ¬P ∧ ¬Q
def de_morgan_1a(hnpq: Implies[[Or[P, Q]], Bottom]) -> And[Implies[[P], Bottom], Implies[[Q], Bottom]]:
    return (lambda hp: hnpq(hp), lambda hq: hnpq(hq))


# ¬P ∧ ¬Q → ¬(P ∨ Q)
def de_morgan_1b(hnpnq: And[Implies[[P], Bottom], Implies[[Q], Bottom]]) -> Implies[[Or[P, Q]], Bottom]:
    return lambda hpq: hnpnq[0](hpq) if isinstance(hpq, P) else hnpnq[1](hpq)


# ¬P ∨ ¬Q → ¬(P ∧ Q) (Type Checker doesn't work correctly)
# def de_morgan_2(hnpnq: Or[Implies[[P], Bottom], Implies[[Q], Bottom]]) -> Implies[[And[P, Q]], Bottom]:
#     return lambda hpq: hnpnq(hpq[0]) if isinstance(hnpnq, Implies[[P], Bottom]) else hnpnq(hpq[1])


# ¬(P ∧ ¬P)
def not_pos_and_neg() -> Implies[[And[P, Implies[[P], Bottom]]], Bottom]:
    return lambda hpnp: hpnp[1](hpnp[0])


# P ∧ ¬Q → ¬(P → Q)
def derive_neg_impl(hpnq: And[P, Implies[[Q], Bottom]]) -> Implies[[Implies[[P], Q]], Bottom]:
    return lambda hpq: hpnq[1](hpq(hpnq[0]))


# ¬P → (P → Q)
def elim_bottom(hnp: Implies[[P], Any]) -> Implies[[P], Q]:
    return lambda hp: hnp(hp)


# ¬P ∧ Q → (P → Q)
def derive_impl(hnpq: And[Implies[[P], Bottom], Q]) -> Implies[[P], Q]:
    return lambda hp: hnpq[0](hp)


# P ∨ ⊥ → P
def never_bottom(hpb: Or[P, Bottom]) -> P:
    return hpb


# ⊥ → P ∧ ⊥
def add_assumption_to_bottom(bottom: Bottom) -> And[P, Bottom]:
    return bottom


# ¬(P ↔︎ ¬P)
def not_pos_iff_neg() -> Implies[[And[Implies[[P], Implies[[P], Bottom]], Implies[[Implies[[P], Bottom]], P]]], Bottom]:
    lemma: Implies[[And[Implies[[P], Implies[[P], Bottom]], Implies[[Implies[[P], Bottom]], P]]], P] = lambda hpnp: hpnp[1](lambda hp: hpnp[0](hp)(hp))
    return lambda hpnp: hpnp[0](lemma(hpnp))(lemma(hpnp))


# (P → Q) → (¬Q → ¬P)
def contraposition(hpq: Implies[[P], Q]) -> Implies[[Implies[[Q], Bottom]], Implies[[P], Bottom]]:
    return lambda hnq: lambda hp: hnq(hpq(hp))
