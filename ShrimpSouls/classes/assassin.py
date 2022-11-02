import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass, field
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

def invis(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def poison_blade(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poison blade.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"invis": invis,
	"poison_blade": poison_blade,
}

class Assassin(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base = 50, level=5, vigor=20)

	def score_acc(self, p):
		return cs.stat_map(p, level=35, faith=10)

	def score_eva(self, p):
		return cs.stat_map(p, level=35, faith=5, dexterity=10)

	def score_att(self, p):
		return cs.stat_map(p, level=35, faith=8, dexterity=8)

	def score_dfn(self, p):
		return cs.stat_map(p, level=18, dexterity=2)



	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []


	@property
	def cl_string(self):
		return "Assassin"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_invis(amt=2)
		self.msg += f"{self.attacker.name} hides in the shadows."


@dataclass
class Target1(actions.DamageTarget):
	statuses: tuple = field(default_factory=lambda:((ss.StatusEnum.poison, random.randint(1, 3)),))

	def __post_init__(self):
		self.score_dmg = utils.score_dmg(m1=2) if self.attacker.invis > 0 else utils.score_dmg()
