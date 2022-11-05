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
		t = env.find_valid_target(u, False, [ss.Positions.FRONT], True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
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
		return cs.stat_map(p, base=100, level=25, vigor=30)
		
	def score_eva(self, p):
		return cs.stat_map(p, level=25, dexterity=6, strength=6)

	def score_acc(self, p):
		return cs.stat_map(p, level=25, dexterity=6)

	def score_att(self, p):
		return cs.stat_map(p, level=32, strength=8, dexterity=8)

	def score_dfn(self, p):
		return cs.stat_map(p, level=32, strength=8, dexterity=8)

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
		