import random
import math
import atexit
import os
import scipy
import functools as ftools

ROLL_THRESHOLD = 30

def compute_bool(a, d, s1, s2):
	s1 = s1.value(a)
	s2 = s2.value(d)

	check = max(min(s1 - s2 + 10, 20), 1)
	roll = random.randint(1, 20)

	return (roll <= check)

def compute_bool_many(a, d, s1, s2, b1=0, b2=0, m1=1, m2=1):
	s1 = m1*s1(a) + b1
	s2 = m2*s2(d) + b2
	r = max(0.5, min(s1/s2, 2))
	p = -0.3 * r**2 + 1.35 * r - 0.55

	rolls = s1//ROLL_THRESHOLD + 1

	total = []
	for d in range(1, rolls + 1):
		total .append((random.random() < p/(d**1.5), s1, s2))

	return total

def __compute_bool_many(a, d, s1, s2, b1=0, b2=0, m1=1, m2=1):
	s1 = m1*s1(a) + b1
	s2 = m2*s2(d) + b2
	diff = s1 - s2

	def recurse(d, bs):		
		if d >= -10:
			check = max(min(d + 10, 20), 1)
			roll = random.randint(1, 20)
			if roll == 20:
				c = True
			elif roll == 1:
				c = False
			else:
				c = roll <= check
			bs.append((c, s1, s2))
			recurse(d-10, bs)
		else:
			check = max(min(d + 10, 20), 1)
			roll = random.randint(1, 20)
			bs.append((roll==20, s1, s2))


	rolls = []
	recurse(diff, rolls)
	return rolls

def compute_num(a, d, s1, s2):
	s1 = s1.value(a)
	s2 = s2.value(d)

	m = min(max(s1 - s2  + 10, 1), 20)

	return (random.randint(1, m), s1, s2)



def compute_dmg(a, d, b1=0, b2=0, m1=1, m2=1):
	dfn = m2 * d.dfn + b2
	att = m1 * a.att + b1
	diff = a.att - d.dfn

	if diff <= 10:
		m = min(max(diff + 10, 1), 20)
		total =  random.randint(1, m)
	else:
		total = 0
		while diff > 10:
			m = min(max(diff + 10, 1), 20)
			total += random.randint(1, m)
			diff -= 10

	return (total, att, dfn)

def compute_dmg(a, d, b1=0, b2=0, m1=1, m2=1):
	dfn = m2 * d.dfn + b2
	att = m1 * a.att + b1
	r = max(0.5, min(att/dfn, 2))
	p = (r**2)/(-3) + 1.5 * r - (2/3)

	return (math.ceil(att * p), att, dfn)

def compute_hit(a, d):
	eva = d.eva
	acc = a.acc

	check = max(min(acc - eva + 10, 20), 1)
	roll = random.randint(1, 20)

	return (roll <= check or d.stun > 0, acc, eva)

RNG_FILE = os.path.join(os.path.split(__file__)[0], "RNG.state")

def write_rng():
	with open(RNG_FILE, 'w') as out:
		out.write(repr(random.getstate()))




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



# Section for maintaining a fixed RNG state.
def read_rng():
	try:
		with open(RNG_FILE, 'r') as out:
			state = eval(out.read())
			random.setstate(state)
	except FileNotFoundError:
		write_rng()

read_rng()

atexit.register(write_rng)