import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math


HEAL_DICE_THRESHOLD = 10

class Priest(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(1.25*p.attributes.faith) + math.ceil(0.25*p.attributes.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 2*p.attributes.faith

	def score_dfn(self, p):
		return math.ceil(p.level*1.25) + math.ceil(p.attributes.faith*2.25)

	def basic_action(self, u, env):
		targets = list(filter(lambda x: not x.dead, env.players))
		targets = random.sample(
			targets, 
			k=min(len(targets), 3 + u.attributes.faith//HEAL_DICE_THRESHOLD),
			counts=[math.ceil(p.max_hp/p.hp) for p in targets])
		targets = list(filter(lambda x: not x.dead, targets))

		return [
			actions.HealTarget(
				attacker=u, 
				defender=t, 
				dmg=random.randint(1, 4)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)) for t in targets
		]
		

	def targeted_action(self, u, target, env):

		if target.dead:
			amt = random.randint(1, 4)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
			return [actions.ReviveTarget(attacker=u, defender=target, dmg=amt)]
		else:
			amt = random.randint(10, 20)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
			return [actions.HealTarget(attacker=u, defender=target, dmg=amt)]

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		if sum(p.hp/p.max_hp for p in party)/len(party) < 0.5:
			party = filter(lambda x: not x.dead, party)
			heal = sum(random.randint(1, 4)  for _ in range((1 + actor.attributes.faith//HEAL_DICE_THRESHOLD)))
			target = min(party, key=lambda p: p.hp)
			return [actions.HealTarget(attacker=actor, defender=target, dmg=heal)]
		else:			
			target = self.find_valid_target(opponents)
			return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Priest"


