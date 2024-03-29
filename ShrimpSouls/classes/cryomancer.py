import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

@dataclass
class Chill(cs.Ability):
	t_amt: int = 3
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=r) for r in t]

@dataclass
class Freeze(cs.Ability):
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class Carapace(cs.Ability):
	t_amt: int = 0

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=u,
				statuses={ss.StatusEnum.briar: lambda: 3})
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"chill": Chill(),
	"freeze": Freeze(),
	"carapace": Carapace(),
}

class Cryomancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=8, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, faith=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10)

	def score_att(self, p):
		return cs.stat_map(p, level=11, faith=1, intelligence=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=11, intelligence=2, faith=2)

	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

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