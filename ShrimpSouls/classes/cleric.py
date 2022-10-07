from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Cleric(ClassSpec):
	def score_acc(self, p):
		return super().score_acc() + 1

	def score_eva(self, p):
		return super().score_eva() - 1

	def score_att(self, p):
		return 3*p.strength+3*p.faith

	def score_def(self, p):
		return 2*p.strength + 3*p.faith

	def basic_action(self, u, players, npcs):
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_defup(amt=2)

		print(f"{u.name} utters a short prayer, bolstering some of their party's defense.")

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