from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Swordsman(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.dexterity*0.65)

	def score_att(self, p):
		return math.ceil(2.5*p.strength + 3.5*p.dexterity)

	def score_def(self, p):
		return 2*p.level + p.strength + p.dexterity

	def basic_action(self, u, players, npcs):
		targets = random.choices(npcs, k=2*(1 + len(npcs)//10))

		for t in targets:
			t.stack_defdown(amt=2)

		print(f"{u.name} hamstrings some of their foes, decreasing their defense.")

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