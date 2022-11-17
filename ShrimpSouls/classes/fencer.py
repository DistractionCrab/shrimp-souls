import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def ripstance(u, targets, env):
	return [Action1(attacker=u,defender=u)]

def taunt(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"ripstance": ripstance,
	"taunt": taunt,
}

class Fencer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	

	def max_hp(self, p):
		
		return cs.stat_map(p, base=100, level=8, vigor=4)

	def score_acc(self, p):
		return cs.stat_map(p, level=12, perception=1, dexterity=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=11, dexterity=2)

	def score_att(self, p):
		return cs.stat_map(p, level=8, dexterity=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, strength=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Fencer"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_ripstance(amt=2)
		self.msg += f"{self.attacker.name} has entered a riposting stance."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_bool(self.attacker, self.defender):
			self.defender.taunt_target(self.attacker)
			self.msg += f"{self.attacker.name} has taunted {self.defender.name} into attacking them. "
		else:
			self.msg += f"{self.attacker.name} has failed to taunt {self.defender.name}. "