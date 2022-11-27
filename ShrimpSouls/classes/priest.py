import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils


def prayer(u, targets, env):
	targets = env.find_valid_target(u, True, True, amt=3)


	return [
		actions.HealTarget(
			attacker=u, 
			defender=t, 
			score=utils.RawScore(m=0.1))
		for t in targets
	]
	

def heal(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, True, True)
		if len(t) == 0:
			return [actions.Error(info="No targets could be found...")]
		t = t[0]
	else:
		t = env.get_target(targets[0])

	if t.dead:
		amt = random.randint(1, 4)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
		return [actions.ReviveTarget(attacker=u, defender=t, score=utils.RawScore(m=1/15))]
	else:
		amt = random.randint(10, 20)*(1 + u.attributes.faith//HEAL_DICE_THRESHOLD)
		return [actions.HealTarget(attacker=u, defender=t, score=utils.RawScore(m=1/5))]

@dataclass
class LightningStorm(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.DamageTarget(
				attacker=u,
				defender=t,
				dmgtype=actions.DamageType.Lightning,
				score_dmg=utils.ScoreDamage(scale=0.5))
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"prayer": prayer,
	"heal": heal,
	"lightningstorm": LightningStorm(),
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
		return cs.stat_map(p, mult=5, base=50, level=8, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=9, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=9, faith=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=8, strength=1)


	def duel_action(self, actor, env):
		party = list(filter(lambda x: not x.dead, env.players.values()))
		heal = sum(random.randint(1, 10)  for _ in range((1 + actor.attributes.faith//HEAL_DICE_THRESHOLD)))
		target = min(party, key=lambda p: p.hp)
		return [
			actions.HealTarget(attacker=actor, defender=target, mult=1/10)
			]

	@property
	def cl_string(self):
		return "Priest"


