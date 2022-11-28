import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass, field
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

@dataclass
class Hamstring(cs.Ability):
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=t)]

@dataclass
class Slice(cs.Ability):
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class Flurry(cs.Ability):
	t_amt: int = 1

	def act(self, u, t, env):
		return [
			actions.DamageTarget(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.bleed: lambda: 1},
				score_dmg=utils.ScoreDamage(scale=0.2))
			for _ in range(4)
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"hamstring": Hamstring(),
	"slice": Slice(),
	"flurry": Flurry(),
}

class Swordsman(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=9, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, level=8, dexterity=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=8, dexterity=2)

	def score_att(self, p):
		return cs.stat_map(p, level=8, dexterity=2, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=8, dexterity=1, strength=2)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]


	@property
	def cl_string(self):
		return "Swordsman"

@dataclass
class Action1(actions.DamageTarget):
	statuses: utils.FrozenDict = utils.FrozenDict({
		ss.StatusEnum.evadown: lambda: random.randint(1,3)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash


@dataclass
class Target1(actions.DamageTarget):
	statuses: utils.FrozenDict = utils.FrozenDict({
		ss.StatusEnum.evadown: lambda: random.randint(1,4)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash
