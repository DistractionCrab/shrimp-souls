import random
import math
import atexit
import os
import scipy
import functools as ftools
import ShrimpSouls as ss
from scipy.special import expit
import persistent

ROLL_THRESHOLD = 30

def acc_scale(self, base):
	if self.accup > 0:
		base *= 1.1
	if self.accdown > 0:
		base *= 0.9
	if self.encourage > 0:
		base *= 1.1
	if self.poison > 0:
		base *= 1.0 - (self.poison * 0.02)

	return math.ceil(base)


def att_scale(self, base):
	if self.attup > 0:
		base *= 1.1
	if self.attdown > 0:
		base *= 0.9
	if self.encourage > 0:
		base *= 1.05
	if self.poison > 0:
		base *= 1.0 - (self.poison * 0.02)

	return math.ceil(base)

def eva_scale(self, base):
	if self.evaup > 0:
		base *= 1.1
	if self.evadown > 0:
		base *= 0.9
	if self.status.stun > 0:
		base *= 0.4

	return math.ceil(base)

def def_scale(self, base):
	if self.defup > 0:
		base *= 1.1
	if self.defdown > 0:
		base *= 0.9
		
	return math.ceil(base)


def score_hit(s1=ss.Scores.Acc, s2=ss.Scores.Eva, b1=0, b2=0, m1=1, m2=1):
	return (s1, s2, b1, b2, m1, m2)

def score_dmg(s1=ss.Scores.Att, s2=ss.Scores.Def, b1=0, b2=0, m1=1, m2=1):
	return (s1, s2, b1, b2, m1, m2)

def compute_prob(a, d, s1=ss.Scores.Acc, s2=ss.Scores.Eva, b1=0, b2=0, m1=1, m2=1):
	s1 = b1 + m1*s1(a)
	s2 = b2 + m2*s2(a)
	
	r = (s1/s2 - 1)*((s1 + s2)/100)
	return expit(r)


def compute_bool_many(a, d, s1=ss.Scores.Acc, s2=ss.Scores.Eva, b1=0, b2=0, m1=1, m2=1):
	p = compute_prob(a, d, s1=s1, s2=s2, b1=b1, b2=b2, m1=m1, m2=m2)
	rolls = 1

	total = []

	return [random.random() < p/(d**1.5) for d in range(1, rolls+1)]

def compute_bool(a, d, s1=ss.Scores.Acc, s2=ss.Scores.Eva, b1=0, b2=0, m1=1, m2=1):
	p = compute_prob(a, d, s1=s1, s2=s2, b1=b1, b2=b2, m1=m1, m2=m2)

	return random.random() < p

def compute_dmg(a, d, s1=ss.Scores.Att, s2=ss.Scores.Def, b1=0, b2=0, m1=1, m2=1):
	p = compute_prob(a, d, s1=s1, s2=s2, b1=b1, b2=b2, m1=m1, m2=m2)
	s1 = m1*s1(a) + b1

	return math.ceil(s1 * p)




class ListGuard:
	def __init__(self, l):
		self.__v = l

	def __iter__(self):
		return iter(self.__v)

	def __getitem__(self, i):
		return self.__v[i]

	def __setitem__(self, i, _):
		raise ValueError("Cannot set item for List Object.")

	def __len__(self):
		return len(self.__v)

	def __str__(self):
		return str(f"Guarded{self.__v}")



class FrozenDict:
	def __init__(self, d):
		self.__d = d

	def __get_item__(self, i):
		return self.__d[i]

	def items(self):
		return self.__d.items()

	def __iter__(self):
		return iter(self.__d)

	def __len__(self):
		return len(self.__d)

	def keys(self):
		return self.__d.keys()

	def values(self):
		return self.__d.values()

	def __str__(self):
		return f"Frozen{self.__d}"

	def __contains__(self, a):
		return a in self.__d
