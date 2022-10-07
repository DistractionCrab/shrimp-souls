from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_acc(self, p):
		return super().score_acc(p)

	def score_att(self, p):
		return 4*p.strength 

	def score_def(self, p):
		return 4*p.strength + 4

	def basic_action(self, u, players, npcs):
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_attup(amt=2)

		print(f"{u.name} emits a powerful warcry, bolstering some of their party.")

	def medium_action(self, u, players, npcs):
		pass

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = random.choices(opponents)[0]

		if super().compute_hit(actor, target):
			dmg = super().compute_dmg(actor, target)

			return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg + actor.strength//10)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of their sword.")]