# These theorems are from https://leanprover.github.io/theorem_proving_in_lean4/propositions_and_proofs.html#examples-of-propositional-validities
from proposition import Or, And, Implies, Iff, Bottom, Not


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
        lambda hp: Or.intro_right(hp),
        lambda hq: Or.intro_left(hq)
    )


# P ∧ Q → Q ∧ P
def and_commutative(hpq: And[P, Q]) -> And[Q, P]:
    return And(hpq.right, hpq.left)


# (P ∨ Q) ∨ R → P ∨ (Q ∨ R)
def or_associative(hpqr: Or[Or[P, Q], R]) -> Or[P, Or[Q, R]]:
    def derive_qr_from_q(hq: Q) -> Or[Q, R]:
        return Or.intro_left(hq)

    def derive_qr_from_r(hr: R) -> Or[Q, R]:
        return Or.intro_right(hr)

    return hpqr.eliminate(
        lambda hpq: hpq.eliminate(
            lambda hp: Or.intro_left(hp),
            lambda hq: Or.intro_right(derive_qr_from_q(hq))
        ),
        lambda hr: Or.intro_right(derive_qr_from_r(hr))
    )


# (P ∧ Q) ∧ R → P ∧ (Q ∧ R)
def and_associative(hpqr: And[And[P, Q], R]) -> And[P, And[Q, R]]:
    return And(hpqr.left.left, And(hpqr.left.right, hpqr.right))


# P ∧ (Q ∨ R) → (P ∧ Q) ∨ (P ∧ R)
def and_distributive_a(hpqr: And[P, Or[Q, R]]) -> Or[And[P, Q], And[P, R]]:
    return hpqr.right.eliminate(
        lambda hq: Or.intro_left(And(hpqr.left, hq)),
        lambda hr: Or.intro_right(And(hpqr.left, hr))
    )


# (P ∧ Q) ∨ (P ∧ R) → P ∧ (Q ∨ R)
def and_distributive_b(hpqpr: Or[And[P, Q], And[P, R]]) -> And[P, Or[Q, R]]:
    return hpqpr.eliminate(
        lambda hpq: And(hpq.left, Or.intro_left(hpq.right)),
        lambda hpr: And(hpr.left, Or.intro_right(hpr.right))
    )


# P ∨ (Q ∧ R) → (P ∨ Q) ∧ (P ∨ R)
def or_distributive_a(hpqr: Or[P, And[Q, R]]) -> And[Or[P, Q], Or[P, R]]:
    return hpqr.eliminate(
        lambda hp: And(Or.intro_left(hp), Or.intro_left(hp)),
        lambda hqr: And(Or.intro_right(hqr.left), Or.intro_right(hqr.right))
    )


# (P ∨ Q) ∧ (P ∨ R) → P ∨ (Q ∧ R)
def or_distributive_b(hpqpr: And[Or[P, Q], Or[P, R]]) -> Or[P, And[Q, R]]:
    def derive_pqr(hp: P) -> Or[P, And[Q, R]]:
        return Or.intro_left(hp)
    
    return hpqpr.left.eliminate(
        lambda hp: derive_pqr(hp),
        lambda hq: hpqpr.right.eliminate(
            lambda hp: Or.intro_left(hp),
            lambda hr: Or.intro_right(And(hq, hr))
        )
    )


# (P → (Q → R)) → (P ∧ Q → R)
def unify_and(hpqr: Implies[P, Implies[Q, R]]) -> Implies[And[P, Q], R]:
    return Implies(lambda hpq:
        hpqr.apply(hpq.left).apply(hpq.right)
    )


# (P ∧ Q → R) → (P → (Q → R))
def destruct_and(hpqr: Implies[And[P, Q], R]) -> Implies[P, Implies[Q, R]]:
    return Implies(lambda hp:
        Implies(lambda hq:
            hpqr.apply(And(hp, hq))
        )
    )


# (P ∨ Q → R) → (P → R) ∧ (Q → R)
def destruct_or(hpqr: Implies[Or[P, Q], R]) -> And[Implies[P, R], Implies[Q, R]]:
    return And(
        Implies(lambda hp: hpqr.apply(Or.intro_left(hp))),
        Implies(lambda hq: hpqr.apply(Or.intro_right(hq)))
    )


# (P → R) ∧ (Q → R) → (P ∨ Q → R)
def unify_or(hprqr: And[Implies[P, R], Implies[Q, R]]) -> Implies[Or[P, Q], R]:
    return Implies(lambda hpq:
        hpq.eliminate(
            lambda hp: hprqr.left.apply(hp),
            lambda hq: hprqr.right.apply(hq)
        )
    )


# ¬(P ∨ Q) → ¬P ∧ ¬Q
def de_morgan_1a(hnpq: Not[Or[P, Q]]) -> And[Not[P], Not[Q]]:
    return And(
        Not(lambda hp: hnpq.apply(Or.intro_left(hp))),
        Not(lambda hq: hnpq.apply(Or.intro_right(hq)))
    )


# ¬P ∧ ¬Q → ¬(P ∨ Q)
def de_morgan_1b(hnpnq: And[Not[P], Not[Q]]) -> Not[Or[P, Q]]:
    return Not(lambda hpq:
        hpq.eliminate(
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
def not_pos_and_neg() -> Not[And[P, Not[P]]]:
    return Not(lambda hpnp:
        hpnp.right.apply(hpnp.left)
    )


# P ∧ ¬Q → ¬(P → Q)
def derive_neg_impl(hpnq: And[P, Not[Q]]) -> Not[Implies[P, Q]]:
    return Not(lambda hpq:
        hpnq.right.apply(hpq.apply(hpnq.left))
    )


# ¬P → (P → Q)
def elim_bottom(hnp: Not[P]) -> Implies[P, Q]:
    return Implies(lambda hp:
        hnp.apply(hp).eliminate()
    )


# ¬P ∧ Q → (P → Q)
def derive_impl(hnpq: And[Not[P], Q]) -> Implies[P, Q]:
    return Implies(lambda hp:
        hnpq.left.apply(hp).eliminate()
    )


# P ∨ ⊥ → P
def never_bottom(hpb: Or[P, Bottom]) -> P:
    return hpb.eliminate(
        lambda hp: hp,
        lambda bottom: bottom.eliminate()
    )


# ⊥ → P ∧ ⊥
def add_assumption_to_bottom(bottom: Bottom) -> And[P, Bottom]:
    return And(bottom.eliminate(), bottom)


# ¬(P ↔︎ ¬P)
def not_pos_iff_neg() -> Not[Iff[P, Not[P]]]:
    def derive_p(hpnp: Iff[P, Not[P]]) -> P:
        return hpnp.backward.apply(
            Not(lambda hp:
                hpnp.forward.apply(hp).apply(hp)
            )
        )
    
    return Not(lambda hpnp:
        hpnp.forward.apply(derive_p(hpnp)).apply(derive_p(hpnp))
    )


# (P → Q) → (¬Q → ¬P)
def contraposition(hpq: Implies[P, Q]) -> Implies[Not[Q], Not[P]]:
    return Implies(lambda hnq:
        Not(lambda hp:
            hnq.apply(hpq.apply(hp))
        )
    )
