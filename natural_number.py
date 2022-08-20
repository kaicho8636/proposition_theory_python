from typing import TypeVar, Generic
S = TypeVar('S')
T = TypeVar('T')


class Refl(Generic[S, T]):
  def __init__(self, left: S, right: T):
    self.left = left
    self.right = right


class Nat:
  pass


M = TypeVar('M', bound=Nat)
N = TypeVar('N', bound=Nat)


class Zero(Nat):
  pass


class Cons(Nat, Generic[N]):
  def __init__(self, prev: N):
    self.prev = prev


def h0(assumption: Refl[Cons[M], N]) -> Refl[Cons[Cons[M]], Cons[N]]: # S+1=T → S+2=T+1
  return Refl(
    Cons(assumption.left),
    Cons(assumption.right)
  )
