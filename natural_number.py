from ast import Sub
from typing import TypeVar, Generic

S = TypeVar('S')
T = TypeVar('T')


class Refl(Generic[S, T]):
    def __init__(self, left: S, right: T):
        self.left = left
        self.right = right


class Nat:
    def __add__(self, other):
        return Add(self, other)


M = TypeVar('M', bound=Nat)
N = TypeVar('N', bound=Nat)


class Zero(Nat):
    pass


class Cons(Nat, Generic[N]):
    def __init__(self, prev: N):
        self.prev = prev


class Add:
    def __init__(self, m: Nat, n: Nat):
        self.m = m
        self.n = n


X = TypeVar('X', bound=Nat)
Y = TypeVar('Y', bound=Nat)
Z = TypeVar('Z', bound=)


test = Add(Cons(Zero()), Zero())


    
