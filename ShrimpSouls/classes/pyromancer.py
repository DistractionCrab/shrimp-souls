from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Pyromancer(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.intelligence) + math.ceil(0.75*p.faith) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(1.25*p.level) + 2

	def score_att(self, p):
		return 3*p.faith+3*p.intelligence

	def score_def(self, p):
		return math.ceil(1.5*p.level) + 3

	def basic_action(self, u, players, npcs):
		targets = random.choices(npcs, k=3*(1 + len(npcs)//10))

		for t in targets:
			t.stack_burn(amt=2)

		print(f"{u.name} unleashes a small pyroclasm to burn some foes.")

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

