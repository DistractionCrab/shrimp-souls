import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass, field
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def hamstring(u, targets, env):
	t = env.find_valid_target(u, False, ss.Positions, True, amt=3)
	return [Action1(attacker=u, defender=r) for r in t]

def slice(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, False, [ss.Positions.FRONT], True)
		if len(t) == 0:
			return [actions.Error(info="No targets could be found...")]
		t = t[0]
	else:
		t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"hamstring": hamstring,
	"slice": slice,
}

class Swordsman(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=9, vigor=5)

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
		ss.Statuses.evadown: lambda: random.randint(1,3)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash


@dataclass
class Target1(actions.DamageTarget):
	statuses: utils.FrozenDict = utils.FrozenDict({
		ss.Statuses.evadown: lambda: random.randint(1,4)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash
