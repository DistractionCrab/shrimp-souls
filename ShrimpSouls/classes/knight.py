import ShrimpSouls.classes as cs
import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import random
import math

def block(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def cover(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"block": block,
	"cover": cover,
}

class Knight(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
		
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=6)

	def score_eva(self, p):
		return cs.stat_map(p, base=9, level=1)
		return super().score_eva(p) - 1

	def score_acc(self, p):
		return cs.stat_map(p, base=11, level=1)

	def score_att(self, p):
		return cs.stat_map(p, strength=3, dexterity=3)

	def score_dfn(self, p):
		return cs.stat_map(p, strength=4, dexterity=4, base=5)
		return p.attributes.strength + 4*p.attributes.dexterity + 5

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]
		

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Knight"


		
@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_block(amt=3)
		self.msg += f"{self.attacker.name} readies their shield to block attacks."


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.stack_block()
		self.attacker.stack_defdown()
		self.attacker.stack_attdown()

		self.msg += f"{self.attacker.name} is covering {self.defender.name}."