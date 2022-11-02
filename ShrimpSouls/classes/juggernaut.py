import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import random
import math

def warcry(u, targets, env):
	targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)
	return [Action1(attacker=u, defender=t) for t in targets]

def shatter(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for shattering.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"warcry": warcry,
	"shatter": shatter,
}

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=25, vigor=35)

	def score_eva(self, p):
		return cs.stat_map(p, level=22, strength=2)

	def score_acc(self, p):
		return cs.stat_map(p, level=22, strength=2)

	def score_att(self, p):
		return cs.stat_map(p, level=35, strength=10)

	def score_dfn(self, p):
		return cs.stat_map(p, level=35, strength=10)


	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

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
	score_dmg: tuple = utils.score_dmg(m1=1.3)
	statuses: tuple = ((ss.StatusEnum.defdown, 3), )
