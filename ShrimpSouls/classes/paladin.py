import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

@dataclass
class Seal(cs.Ability):
	t_amt: int = 0
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=u)]

@dataclass
class Censure(cs.Ability):
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class Judgement(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.stun: lambda: 1})
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"sealing": Seal(),
	"censure": Censure(),
	"judgement": Judgement(),
}

class Paladin(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base = 100, level=12, vigor=4)

	def score_acc(self, p):
		return cs.stat_map(p, level=9, faith=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=8, strength=1, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=11, strength=2, faith=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=11, faith=1, strength=2)

	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Paladin"

@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnum.sealing.stack(self.attacker, amt=3)
		self.msg += f"{self.attacker.name} casts a prayer on their blade to seal their foes."


@dataclass
class Target1(actions.EffectAction):
	def on_hit(self):
		ss.StatusEnum.attdown.stack(self.defender, amt=2)
		ss.StatusEnum.evadown.stack(self.defender, amt=2)
		ss.StatusEnum.defdown.stack(self.defender, amt=2)
		ss.StatusEnum.accdown.stack(self.defender, amt=2)

		self.msg += f"{self.attacker.name} has weakened {self.defender.name} with a holy censure."

	def on_miss(self):
		self.msg += f"{self.defender.name} maintains their conviction against {self.attacker.name}'s censure."
