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
	t = env.find_valid_target(u, True, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

@dataclass
class Block(cs.Ability):
	t_amt: int = 0
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=u)]

@dataclass
class Cover(cs.Ability):
	allyq: bool = True
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class RipStance(cs.Ability):
	t_amt: int = 0

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=u,
				statuses={ss.StatusEnum.ripstance: lambda: 2})
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"block": Block(),
	"cover": Cover(),
	"ripstance": RipStance(),
}

class Knight(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP	
		
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=10, vigor=5)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, dexterity=1, perception=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, dexterity=1, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, strength=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Knight"


		
@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnum.block.stack(self.attacker, amt=3)
		self.msg += f"{self.attacker.name} readies their shield to block attacks."


@dataclass
class Target1(actions.Action):
	def apply(self):
		ss.StatusEnum.block.stack(self.defender)

		self.msg += f"{self.attacker.name} is covering {self.defender.name}."