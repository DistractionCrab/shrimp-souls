import ShrimpSouls as ss
import random
import functools as ftools
import atexit
import os

def compute_bool(a, d, s1, s2):
	s1 = s1.value(a)
	s2 = s2.value(d)

	check = max(min(s1 - s2 + 10, 20), 1)
	roll = random.randint(1, 20)

	return (roll <= check)

def compute_bool_many(a, d, s1, s2):
	s1 = s1(a)
	s2 = s2(d)
	diff = s2 - s1

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

def compute_dmg(a, d):
	dfn = d.dfn
	att = a.att

	m = min(max(a.att - d.dfn  + 10, 1), 20)

	return (random.randint(1, m), att, dfn)

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

def read_rng():
	try:
		with open(RNG_FILE, 'r') as out:
			state = eval(out.read())
			random.setstate(state)
	except FileNotFoundError:
		write_rng()

read_rng()

atexit.register(write_rng)