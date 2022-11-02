import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def sealing(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def censure(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"sealing": sealing,
	"censure": censure,
}

class Paladin(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=6)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=1)

	def score_eva(self, p):
		return cs.stat_map(p, base=8, level=1)

	def score_att(self, p):
		return cs.stat_map(p, strength=3, faith=4)

	def score_dfn(self, p):
		return cs.stat_map(p, faith=3.5, strength=3.5)

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Paladin"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_sealing(amt=3)
		self.msg += f"{self.attacker.name} casts a prayer on their blade to seal their foes."


@dataclass
class Target1(actions.EffectAction):
	def on_hit(self):
		self.defender.stack_attdown(amt=2)
		self.defender.stack_evadown(amt=2)
		self.defender.stack_defdown(amt=2)
		self.defender.stack_accdown(amt=2)

		self.msg += f"{self.attacker.name} has weakened {self.defender.name} with a holy censure."

	def on_miss(self):
		self.msg += f"{self.defender.name} maintains their conviction against {self.attacker.name}'s censure."
