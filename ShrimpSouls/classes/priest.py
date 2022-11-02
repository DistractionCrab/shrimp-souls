import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math

def prayer(u, targets, env):
	targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)


	return [
		actions.HealTarget(
			attacker=u, 
			defender=t, 
			dmg=random.randint(1, 4)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)) for t in targets
	]
	

def heal(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	target = env.get_target(targets[0])

	if target.dead:
		amt = random.randint(1, 4)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
		return [actions.ReviveTarget(attacker=u, defender=target, dmg=amt)]
	else:
		amt = random.randint(10, 20)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
		return [actions.HealTarget(attacker=u, defender=target, dmg=amt)]

ABI_MAP = {
	"prayer": prayer,
	"heal": heal,
}

HEAL_DICE_THRESHOLD = 10

class Priest(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def position(self):
		return ss.Positions.BACK


	def max_hp(self, p):
		return cs.stat_map(p, base=10, level=2, vigor=2)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, faith=1.25, dexterity=0.25)

	def score_eva(self, p):
		return cs.stat_map(p, base=12, level=1)

	def score_att(self, p):
		return cs.stat_map(p, faith=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=1.25, faith=2.25)


	def duel_action(self, actor, env):
		party = list(filter(lambda x: not x.dead, env.players.values()))
		heal = sum(random.randint(1, 10)  for _ in range((1 + actor.attributes.faith//HEAL_DICE_THRESHOLD)))
		target = min(party, key=lambda p: p.hp)
		return [
			actions.HealTarget(attacker=actor, defender=target, dmg=heal)
			]

	@property
	def cl_string(self):
		return "Priest"


