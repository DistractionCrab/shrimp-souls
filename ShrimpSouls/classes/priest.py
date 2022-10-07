import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math


HEAL_DICE_THRESHOLD = 10

class Priest(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(1.25*p.intelligence) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 2*p.faith

	def score_def(self, p):
		return math.ceil(p.level*1.25)

	def basic_action(self, u, players, npcs):
		targets = set(random.choices(
			players, 
			k=3*(1 + len(players)//10),
			weights=[1/(1 + p.health) for p in players]))

		for t in targets:
			t.damage(-(random.randint(1, 4)*(1 + u.faith/HEAL_DICE_THRESHOLD)))

		print(f"{u.name} has healed {', '.join(t.name for t in targets)}.")

		

	def medium_action(self, u, players, npcs):
		pass

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		

		if super().compute_hit(actor, target):
			if sum(p.health/p.max_health for p in party)/len(party) < 0.5:
				party = filter(lambda x: not p.dead, party)
				heal = sum(random.randint(1, 4)  for _ in range((1 + actor.faith//HEAL_DICE_THRESHOLD)))
				target = min(party, key=lambda p: p.health)
				return [actions.HealTarget(attacker=actor, defender=target, dmg=heal)]
			else:
				target = self.find_valid_target(opponents)
				dmg = super().compute_dmg(actor, target)

				return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of their sword.")]