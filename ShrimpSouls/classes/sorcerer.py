from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Sorcerer(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(1.25*p.intelligence) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 4*p.intelligence +3

	def score_def(self, p):
		return math.ceil(p.level*1.25)

	def basic_action(self, u, party, opponents):
		u.stack_soulmass(amt=3)
		print(f"{u.name} summons a phalanx of soulmasses to defend themselves.")

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