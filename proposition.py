from typing import Any, TypeVar, Generic
from collections.abc import Callable
from abc import ABCMeta, abstractmethod


# ∀ S T U
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


# S ∨ T
class Or(Generic[S, T], metaclass=ABCMeta):
    @abstractmethod
    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        ...


# Construct S ∨ T from S
class Left(Or[S, T]):
    def __init__(self, left: S):
        self.left = left

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return left_case(self.left)


# Construct S ∨ T from T
class Right(Or[S, T]):
    def __init__(self, right: T):
        self.right = right

    def eliminate(self, left_case: Callable[[S], U], right_case: Callable[[T], U]) -> U:
        return right_case(self.right)


# S ∧ T
class And(Generic[S, T]):
    def __init__(self, left: S, right: T):
        self.left = left
        self.right = right


# S → T
class Implies(Generic[S, T]):
    def __init__(self, mapping: Callable[[S], T]):
        self.apply = mapping


# ⊥
class Bottom:
    def eliminate(self) -> Any:
        return


# ¬S
class Not(Implies[S, Bottom]):
    pass


# P Q R: Proposition
class P:
    pass


class Q:
    pass


class R:
    pass


# P ∨ Q → Q ∨ P
def or_commutative(hpq: Or[P, Q]) -> Or[Q, P]:
    return hpq.eliminate(
        lambda hp: Right(hp),
        lambda hq: Left(hq)
    )


# P ∧ Q → Q ∧ P
def and_commutative(hpq: And[P, Q]) -> And[Q, P]:
    return And(hpq.right, hpq.left)


# (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
def or_associative(hpqr: Or[Or[P, Q], R]) -> Or[P, Or[Q, R]]:
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


# (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
def and_associative(hpqr: And[And[P, Q], R]) -> And[P, And[Q, R]]:
    return And(
        hpqr.left.left,
        And(
            hpqr.left.right,
            hpqr.right
        )
    )


# P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R)
def and_distributive_a(hpqr: And[P, Or[Q, R]]) -> Or[And[P, Q], And[P, R]]:
    return hpqr.right.eliminate(
        lambda hq: Left(And(hpqr.left, hq)),
        lambda hr: Right(And(hpqr.left, hr))
    )


# (P ∧ Q) ∨ (P ∧ R) → P ∧ (Q ∨ R)
def and_distributive_b(hpqpr: Or[And[P, Q], And[P, R]]) -> And[P, Or[Q, R]]:
    return hpqpr.eliminate(
        lambda hpq: And(hpq.left, Left(hpq.right)),
        lambda hpr: And(hpr.left, Right(hpr.right))
    )


# P ∨ (Q ∧ R) → (P ∨ Q) ∧ (P ∨ R)
def or_distributive_a(hpqr: Or[P, And[Q, R]]) -> And[Or[P, Q], Or[P, R]]:
    return hpqr.eliminate(
        lambda hp: And(Left(hp), Left(hp)),
        lambda hqr: And(Right(hqr.left), Right(hqr.right))
    )


# (P ∨ Q) ∧ (P ∨ R) → P ∨ (Q ∧ R)
def or_distributive_b(hpqpr: And[Or[P, Q], Or[P, R]]) -> Or[P, And[Q, R]]:
    def derive_pqr(hp: P) -> Or[P, And[Q, R]]:
        return Left(hp)
    
    return hpqpr.left.eliminate(
        lambda hp: derive_pqr(hp),
        lambda hq: hpqpr.right.eliminate(
            lambda hp: Left(hp),
            lambda hr: Right(And(hq, hr))
        )
    )


# (P → (Q → R)) → (P ∧ Q → R)
def unify_and(hpqr: Implies[P, Implies[Q, R]]) -> Implies[And[P, Q], R]:
    return Implies(
        lambda hpq: hpqr
        .apply(hpq.left)
        .apply(hpq.right)
        )


# (P ∧ Q → R) → (P → (Q → R))
def destruct_and(hpqr: Implies[And[P, Q], R]) -> Implies[P, Implies[Q, R]]:
    return Implies(
        lambda hp: Implies(
            lambda hq: hpqr.apply(And(hp, hq))
        )
    )


# (P ∨ Q → R) → (P → R) ∧ (Q → R)
def destruct_or(hpqr: Implies[Or[P, Q], R]) -> And[Implies[P, R], Implies[Q, R]]:
    return And(
        Implies(lambda hp: hpqr.apply(Left(hp))),
        Implies(lambda hq: hpqr.apply(Right(hq)))
    )


# (P → R) ∧ (Q → R) → (P ∨ Q → R)
def unify_or(hprqr: And[Implies[P, R], Implies[Q, R]]) -> Implies[Or[P, Q], R]:
    return Implies(
        lambda hpq: hpq.eliminate(
            lambda hp: hprqr.left.apply(hp),
            lambda hq: hprqr.right.apply(hq)
        )
    )


# ¬(P ∨ Q) → ¬P ∧ ¬Q
def de_morgan_1a(hnpq: Implies[Or[P, Q], Bottom]) -> And[Implies[P, Bottom], Implies[Q, Bottom]]:
    return And(
        Implies(lambda hp: hnpq.apply(Left(hp))),
        Implies(lambda hq: hnpq.apply(Right(hq)))
    )


# ¬P ∧ ¬Q → ¬(P ∨ Q)
def de_morgan_1b(hnpnq: And[Not[P], Not[Q]]) -> Not[Or[P, Q]]:
    return Not(
        lambda hpq: hpq.eliminate(
            lambda hp: hnpnq.left.apply(hp),
            lambda hq: hnpnq.right.apply(hq)
        )
    )


# ¬P ∨ ¬Q → ¬(P ∧ Q)
def de_morgan_2(hnpnq: Or[Not[P], Not[Q]]) -> Not[And[P, Q]]:
    return hnpnq.eliminate(
        lambda hnp: Not(lambda hpq: hnp.apply(hpq.left)),
        lambda hnq: Not(lambda hpq: hnq.apply(hpq.right))
    )


# ¬(P ∧ ¬P)
not_contradiction: Not[And[P, Not[P]]] = Not(
    lambda hpnp: hpnp.right.apply(hpnp.left)
)


# P ∧ ¬Q → ¬(P → Q)
def derive_neg_impl(hpnq: And[P, Not[Q]]) -> Not[Implies[P, Q]]:
    return Not(
        lambda hpq: hpnq.right.apply(
            hpq.apply(hpnq.left)
        )
    )


# ¬P → (P → Q)
def elim_bottom(hnp: Not[P]) -> Implies[P, Q]:
    return Implies(lambda hp: hnp.apply(hp).eliminate())


# ¬P ∧ Q → (P → Q)
def derive_impl(hnpq: And[Not[P], Q]) -> Implies[P, Q]:
    return Implies(lambda hp: hnpq.left.apply(hp).eliminate())


# P ∨ ⊥ → P
def never_bottom(hpb: Or[P, Bottom]) -> P:
    return hpb.eliminate(
        lambda hp: hp,
        lambda bottom: bottom.eliminate()
    )


# ⊥ → P ∧ ⊥
def add_assumption_to_bottom(bottom: Bottom) -> And[P, Bottom]:
    return And(bottom.eliminate(), bottom)


# (P → Q) → (¬Q → ¬P)
def contraposition(hpq: Implies[P, Q]) -> Implies[Not[Q], Not[P]]:
    return Implies(
        lambda hnq: Not(
            lambda hp: hnq.apply(hpq.apply(hp))
        )
    )
