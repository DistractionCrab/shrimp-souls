import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import random
import math

def warcry(u, targets, env):
	t = env.find_valid_target(u, True, True, amt=3)
	return [Action1(attacker=u, defender=r) for r in t]

def shatter(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"warcry": warcry,
	"shatter": shatter,
}

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=12, vigor=6)

	def score_eva(self, p):
		return cs.stat_map(p, level=8, strength=1, dexterity=1)

	def score_acc(self, p):
		return cs.stat_map(p, level=9, perception=1)

	def score_att(self, p):
		return cs.stat_map(p, level=11, strength=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=11, strength=2, vigor=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Juggernaut"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_attup(amt=3)
		self.msg += f"{self.attacker.name} warcry boosts {self.defender.name}'s attack."


@dataclass
class Target1(actions.DamageTarget):
	score_hit: tuple = utils.score_hit(m1=0.9)
	score_dmg: tuple = utils.score_dmg(m1=1.3)
	statuses: utils.FrozenDict =  utils.FrozenDict({
		ss.StatusEnum.defdown: lambda: random.randint(1, 4)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Strike
