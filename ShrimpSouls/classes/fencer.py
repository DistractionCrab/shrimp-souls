from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Fencer(ClassSpec):
	def score_acc(self, p):
		return 12 + math.ceil(1.5*p.dexterity)

	def score_eva(self, p):
		return 12 + math.ceil(1.5*p.dexterity)

	def score_att(self, p):
		return math.ceil(3.5*p.dexterity)

	def score_def(self, p):
		return p.level + 2*p.dexterity

	def basic_action(self, u, players, npcs):
		u.stack_ripstance()
		print(f"{u.name} has entered a riposting stance.")

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