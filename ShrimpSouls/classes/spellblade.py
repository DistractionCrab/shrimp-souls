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
		t = env.find_valid_target(u, True, ss.Positions, True)
		if len(t) == 0:
			return [actions.Error(info="No targets could be found...")]
		t = t[0]
	else:
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


	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=10, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, intelligence=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, strength=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, intelligence=1, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, intelligence=1, strength=1)



	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Spellblade"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_attup(amt=2)
		self.attacker.stack_defup(amt=2)
		self.msg += f"{self.attacker.name} enchants their sword and shield, enhancing their attack and defense."


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.stack_block()
		self.defender.stack_soulmass()
		self.attacker.stack_defdown()
		self.attacker.stack_evadown()

		self.msg += f"{self.attacker.name} is covering {self.defender.name} with a magical defense."