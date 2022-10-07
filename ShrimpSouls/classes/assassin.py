from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Assassin(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.dexterity/2)

	def score_eva(self, p):
		return 12 + math.ceil(1.25*p.dexterity) + math.ceil(1.25*p.faith)

	def score_att(self, p):
		return math.ceil(2.5*p.faith + 3.5*p.dexterity)

	def score_def(self, p):
		return p.level + 2*p.dexterity

	def basic_action(self, u, players, npcs):
		u.stack_invis()
		print(f"{u.name} hides in the shadows.")

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