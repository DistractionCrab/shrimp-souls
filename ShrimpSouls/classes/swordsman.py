import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass, field
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def hamstring(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def slice(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, False, [ss.Positions.FRONT], True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
		t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"hamstring": hamstring,
	"slice": slice,
}

class Swordsman(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=20, vigor=20)

	def score_acc(self, p):
		return cs.stat_map(p, level=25, dexterity=6)

	def score_eva(self, p):
		return cs.stat_map(p, level=25, dexterity=5)

	def score_att(self, p):
		return cs.stat_map(p, level=22, dexterity=2)

	def score_dfn(self, p):
		return cs.stat_map(p, level=22, dexterity=4)


	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [
				actions.DamageTarget(attacker=actor, defender=target),
				actions.DamageTarget(attacker=actor, defender=target)
			]
		else:
			return []


	@property
	def cl_string(self):
		return "Swordsman"

@dataclass
class Action1(actions.DamageTarget):
	statuses: tuple = ((ss.Statuses.evadown, 2),)


@dataclass
class Target1(actions.DamageTarget):
	statuses: tuple = field(default_factory=lambda:(ss.StatusEnum.bleed, random.randint(1,2)))
