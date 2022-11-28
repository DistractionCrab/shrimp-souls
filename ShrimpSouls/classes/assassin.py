import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass, field
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils


@dataclass
class Hide(cs.Ability):
	t_amt: int = 0
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=u)]

@dataclass
class PoisonedBlade(cs.Ability):
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class SmokeBomb(cs.Ability):
	t_amt: int = 3
	allyq: bool = True

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.invis: lambda: 2})
			for t in targets
		]



ABI_MAP = {
	"autoattack": cs.autoattack,
	"invis": Hide(),
	"poison_blade": PoisonedBlade(),
	"smokebomb": SmokeBomb()
}

class Assassin(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=8, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=11, faith=1, perception=2)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=2)

	def score_att(self, p):
		return cs.stat_map(p, level=11, faith=2, dexterity=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=8, dexterity=1)



	def duel_action(self, actor, env):
		if actor.invis == 0:
			return [
				actions.DamageTarget(attacker=actor, defender=t) 
				for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]
		else:
			return []


	@property
	def cl_string(self):
		return "Assassin"


@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnum.invis.stack(self.attacker, amt=2)
		self.msg += f"{self.attacker.name} hides in the shadows."


@dataclass
class Target1(actions.DamageTarget):
	statuses: utils.FrozenDict =  utils.FrozenDict({
		ss.StatusEnum.poison: lambda: random.randint(1, 3)
	})
	abilityrange: actions.AbilityRange = actions.AbilityRange.Close
	dmgtype: actions.DamageType = actions.DamageType.Pierce

	def __post_init__(self):
		self.score_dmg = utils.ScoreDamage(m1=1.7) if self.attacker.status.invis > 0 else utils.ScoreDamage()
