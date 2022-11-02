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
		return [actions.Error(info=f"No targets specified for poaching.")]
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
		return cs.stat_map(p, base=20, level=4, vigor=4)
		return 20 + 4*p.level + 4*p.attributes.vigor

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=0.5, dexterity=0.5)
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return cs.stat_map(p, base=10, level=0.35, dexterity=0.65)
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.attributes.dexterity*0.65)

	def score_att(self, p):
		return cs.stat_map(p, strength=2.5, dexterity=3.5)
		return math.ceil(2.5*p.attributes.strength + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return cs.stat_map(p, level=2, strength=1, dexterity=1)
		return 2*p.level + p.attributes.strength + p.attributes.dexterity


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
