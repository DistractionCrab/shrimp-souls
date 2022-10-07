from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Cryomancer(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.intelligence) + math.ceil(0.75*p.faith) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(0.75*p.level) + 2

	def score_att(self, p):
		return 3*p.faith+3*p.intelligence

	def score_def(self, p):
		return 3 + 2*(p.faith + p.intelligence)

	def basic_action(self, u, players, npcs):
		targets = random.choices(npcs, k=3*(1 + len(npcs)//10))

		for t in targets:
			t.stack_defdown()
			t.stack_attdown()

		print(f"{u.name} conjures a frozen fog that chills their foes, lowering their defense and attack.")

	def medium_action(self, u):
		pass

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = random.choices(opponents)[0]

		if super().compute_hit(actor, target):
			dmg = super().compute_dmg(actor, target)

			return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of their sword.")]