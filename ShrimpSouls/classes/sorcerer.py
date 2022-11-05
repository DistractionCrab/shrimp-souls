from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def soulmass(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def soulspear(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, False, ss.Positions, True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
		t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"soulmass": soulmass,
	"soulspear": soulspear,
}


class Sorcerer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	@property
	def position(self):
		return ss.Positions.BACK
		
	def max_hp(self, p):
		return cs.stat_map(p, base=50, level=10, vigor=10)

	def score_acc(self, p):
		return cs.stat_map(p, level=25, intelligence=5)

	def score_eva(self, p):
		return cs.stat_map(p, level=25)

	def score_att(self, p):
		return cs.stat_map(p, level=35, intelligence=10)

	def score_dfn(self, p):
		return cs.stat_map(p, level=25)


	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Sorcerer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_soulmass(amt=2)
		self.msg += f"{self.attacker.name} summons a phalanx of soulmasses to defend themselves."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.5)