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
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for armor_breaking.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"sharpen": sharpen,
	"armor_break": armor_break,
}

class Warrior(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=6)
		
	def score_eva(self, p):
		return cs.stat_map(p, base=10, level=0.5, dexterity=0.5)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=1, dexterity=0.5)

	def score_att(self, p):
		return cs.stat_map(p, strength=3.5, dexterity=2.5)

	def score_dfn(self, p):
		return cs.stat_map(p, level=2, strength=1, dexterity=1)

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

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

	def on_hit(self):
		self.defender.use_defup(self.defender.defup)
		self.defender.use_evaup(self.defender.evaup)

		self.msg += f"{self.attacker.name}'s armor break removed {self.defender.name}'s defensive buffs."
		