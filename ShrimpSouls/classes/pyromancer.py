from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def pyroclasm(u, targets, env):
	t = env.find_valid_target(u, False, True, amt=3)
	return [Action1(attacker=u, defender=r) for r in t]

def fireball(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

@dataclass
class SmokeScreen(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.accdown: lambda: 2})
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"pyroclasm": pyroclasm,
	"fireball": fireball,
	"smokescreen": SmokeScreen(),
}

class Pyromancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base = 100, level=8, vigor=3)	

	def score_acc(self, p):
		return cs.stat_map(p, level=10, intelligence=1, faith=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=11, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, intelligence=2, faith=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=8, strength=1)

	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Pyromancer"

@dataclass
class Action1(actions.StatusAction):
	statuses: utils.FrozenDict = utils.FrozenDict({
		ss.StatusEnum.burn:  lambda: random.randint(1, 3)
	})


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.3)
	statuses: utils.FrozenDict = utils.FrozenDict({
		ss.StatusEnum.burn:  lambda: 2
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Medium
	dmgtype: actions.DamageType = actions.DamageType.Fire