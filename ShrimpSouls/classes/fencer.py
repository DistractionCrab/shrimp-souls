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

@dataclass
class RipStance(cs.Ability):
	t_amt: int = 0

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=u,
				statuses={ss.StatusEnum.ripstance: lambda: 4})
		]

@dataclass
class FanOfBlades(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.DamageTarget(
				attacker=u,
				defender=t,
				dmgtype=actions.DamageType.Pierce,
				abilityrange=actions.AbilityRange.Long,
				statuses={ss.StatusEnum.evadown: lambda: 1},
				score_dmg=utils.ScoreDamage(scale=0.5))
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"ripstance": RipStance(),
	"taunt": taunt,
	"fanofblades": FanOfBlades(),
}

class Fencer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	

	def max_hp(self, p):
		
		return cs.stat_map(p, mult=5, base=100, level=8, vigor=4)

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
class Target1(actions.Action):
	def apply(self):
		if utils.compute_bool(self.attacker, self.defender):
			self.defender.taunt_target(self.attacker)
			self.msg += f"{self.attacker.name} has taunted {self.defender.name} into attacking them. "
		else:
			self.msg += f"{self.attacker.name} has failed to taunt {self.defender.name}. "