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
		t = env.find_valid_target(u, True, ss.Positions, True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
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
	
		
	def max_hp(self, p):
		return cs.stat_map(p, base =100, level=10, vigor=5)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, dexterity=1, perception=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, dexterity=1, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, strength=1)


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