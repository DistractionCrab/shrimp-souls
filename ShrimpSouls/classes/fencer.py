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
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for taunting.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"ripstance": ripstance,
	"taunt": taunt,
}

class Fencer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	

	def max_hp(self, p):
		
		return cs.stat_map(p, base=100, level=10, vigor=25)

	def score_acc(self, p):
		return cs.stat_map(p, level=35, dexterity=10)

	def score_eva(self, p):
		return cs.stat_map(p, level=35, dexterity=8)

	def score_att(self, p):
		return cs.stat_map(p, level=22, dexterity=4)

	def score_dfn(self, p):
		return cs.stat_map(p, level=22, dexterity=2)


	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

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
		if utils.compute_hit(self.attacker, self.defender):
			self.defender.taunt_target(self.attacker)
			self.msg += f"{self.attacker.name} has taunted {self.defender.name} into attacking them. "
		else:
			self.msg += f"{self.attacker.name} has failed to taunt {self.defender.name}. "