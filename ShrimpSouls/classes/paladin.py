from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Paladin(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p)

	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_att(self, p):
		return math.ceil(3*p.strength) + math.ceil(4*p.faith)

	def score_def(self, p):
		return 4 + math.ceil(3.5*p.faith) + math.ceil(3.5*p.strength)

	def basic_action(self, u, players, npcs):
		u.stack_sealing(amt=3)
		print(f"{u.name} casts a prayer on their blade to seal their foes.")

	def medium_action(self, u, players, npcs):
		pass

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = random.choices(opponents)[0]

		if super().compute_hit(actor, target):
			dmg = super().compute_dmg(actor, target)

			return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of their sword.")]