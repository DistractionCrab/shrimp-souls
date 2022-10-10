import ShrimpSouls as ss

def compute_bool(a, d, s1, s2):
	s1 = s1.value(a)
	s2 = s2.value(d)

	check = max(min(s2 - s1 + 10, 20), 1)
	roll = ss.roll_dice(1)[0]

	return (roll != 1 and roll > check) or roll == 20


def compute_dmg(a, d):
	dfn = d.dfn
	att = a.att

	m = min(max(d.dfn - a.att + 10, 1), 20)

	return ss.roll_dice(max_r=m)[0]

def compute_hit(a, d):
	eva = d.eva
	acc = a.acc

	check = max(min(eva - acc + 10, 20), 1)
	roll = ss.roll_dice(1)[0]

	return (roll != 1 and roll > check) or roll == 20