import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import random
import math

class SpellBlade(ClassSpec):
	def max_hp(self, p):
		return 20 + 5*p.level + 6*p.attributes.vigor

	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_att(self, p):
		return 3*p.attributes.strength+3*p.attributes.intelligence

	def score_dfn(self, p):
		return 2*p.attributes.strength + 3*p.attributes.intelligence

	def basic_action(self, u, env):
		
		return [Action1(attacker=u,defender=u)]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u,defender=target)]

		

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
		self.attacker.stack_accdown()

		self.msg += f"{self.attacker.name} is covering {self.defender.name} with a magical defense."