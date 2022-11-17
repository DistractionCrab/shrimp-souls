from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def soulmass(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def soulspear(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"soulmass": soulmass,
	"soulspear": soulspear,
}


class Sorcerer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=8, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, intelligence=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=9, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=11, intelligence=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=8, strength=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Sorcerer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_soulmass(amt=2)
		self.msg += f"{self.attacker.name} summons a phalanx of soulmasses to defend themselves."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.5)
	abilityrange: actions.AbilityRange = actions.AbilityRange.Long
	dmgtype: actions.DamageType = actions.DamageType.Magic