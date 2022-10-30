import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import random
import math


def enchant(u, targets, env):		
	return [Action1(attacker=u,defender=u)]

def magic_cover(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for Magic Cover.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u,defender=t)]

ABI_MAP = {
	"enchant": enchant,
	"magic_cover": magic_cover,
}

class SpellBlade(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP

	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())

	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=6)
		return 20 + 5*p.level + 6*p.attributes.vigor

	def score_acc(self, p):
		return cs.stat_map(p, base=11, level=1)
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return cs.stat_map(p, base=9, level=1)
		return super().score_eva(p) - 1

	def score_att(self, p):
		return cs.stat_map(p, strength=3, intelligence=3)
		return 3*p.attributes.strength+3*p.attributes.intelligence

	def score_dfn(self, p):
		return cs.stat_map(p, strength=4, intelligence=4)
		return 2*p.attributes.strength + 3*p.attributes.intelligence

	def basic_action(self, u, env):		
		return [Action1(attacker=u,defender=u)]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u,defender=target)]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Spellblade"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_attup(amt=2)
		self.attacker.stack_defup(amt=2)
		self.msg += f"{self.attacker.name} enchantes their sword and shield, enhancing their attack and defense."


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.stack_block()
		self.defender.stack_soulmass()
		self.attacker.stack_defdown()
		self.attacker.stack_evadown()

		self.msg += f"{self.attacker.name} is covering {self.defender.name} with a magical defense."