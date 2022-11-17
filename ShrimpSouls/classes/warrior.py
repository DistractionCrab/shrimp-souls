import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def sharpen(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def armor_break(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

	

ABI_MAP = {
	"autoattack": cs.autoattack,
	"sharpen": sharpen,
	"armor_break": armor_break,
}

class Warrior(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=11, vigor=4)
		
	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, perception=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=9, strength=1, dexterity=1)

	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Warrior"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_attup(amt=3)
		self.msg += f"{self.attacker.name} sharpens their blade, increasing their attack."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.2)
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash

	def on_hit(self):
		self.defender.use_defup(self.defender.defup)
		self.defender.use_evaup(self.defender.evaup)

		self.msg += f"{self.attacker.name}'s armor break removed {self.defender.name}'s defensive buffs."
		