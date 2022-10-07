from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class SpellBlade(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_att(self, p):
		return 3*p.strength+3*p.intelligence

	def score_def(self, p):
		return 2*p.strength + 3*p.intelligence

	def basic_action(self, u, party, opponents):
		u.stack_attup()
		u.stack_defup()
		print(f"{u.name} enchants their sword and shield enhancing their attack and defense.")

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