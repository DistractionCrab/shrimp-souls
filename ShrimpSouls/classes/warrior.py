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

@dataclass
class Whirlwind(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.DamageTarget(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.bleed: lambda: 3},
				score_dmg=utils.ScoreDamage(scale=0.5))
			for t in targets
		]

	

ABI_MAP = {
	"autoattack": cs.autoattack,
	"sharpen": sharpen,
	"armor_break": armor_break,
	"whirlwind": Whirlwind(),
}

class Warrior(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=11, vigor=4)
		
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
		ss.StatusEnum.attup.stack(self.attacker, amt=3)
		self.msg += f"{self.attacker.name} sharpens their blade, increasing their attack."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.ScoreDamage(m1=1.2)
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Slash

	def on_hit(self):
		ss.StatusEnum.defup.use(self.defender, self.defender.status.defup)
		ss.StatusEnum.evaup.use(self.defender, self.defender.status.evaup)

		self.msg += f"{self.attacker.name}'s armor break removed {self.defender.name}'s defensive buffs."
		