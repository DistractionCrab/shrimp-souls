import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

def chill(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def freeze(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, False, [ss.Positions.FRONT], True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
		t = env.get_target(targets[0])
		
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"chill": chill,
	"freeze": freeze,
}

class Cryomancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=8, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, faith=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10)

	def score_att(self, p):
		return cs.stat_map(p, level=11, faith=1, intelligence=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=11, intelligence=2, faith=2)

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Cryomancer"


@dataclass
class Action1(actions.StatusAction):
	statuses: utils.FrozenDict =  utils.FrozenDict({
		ss.StatusEnum.evadown: lambda: random.randint(1, 3),
		ss.StatusEnum.attdown: lambda: random.randint(1, 3),
	})


@dataclass
class Target1(actions.StatusAction):
	statuses: utils.FrozenDict =  utils.FrozenDict({
		ss.StatusEnum.stun: lambda: random.randint(1, 4)
	})