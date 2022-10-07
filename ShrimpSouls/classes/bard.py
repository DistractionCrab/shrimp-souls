from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Bard(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 2

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.dexterity*0.65)

	def score_att(self, p):
		return p.dexterity + p.intelligence + p.perception + p.luck

	def score_def(self, p):
		return math.ceil(1.5*p.level) + 3

	def basic_action(self, u, players, npcs):
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_encourage()

		print(f"{u.name} plays a wartime ballad, encouraging some of their party.")

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