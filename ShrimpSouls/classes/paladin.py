from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Paladin(ClassSpec):
	def max_hp(self, p):
		return 20 + 5*p.level + 6*p.attributes.vigor

	def score_acc(self, p):
		return super().score_acc(p)

	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_att(self, p):
		return math.ceil(3*p.attributes.strength) + math.ceil(4*p.attributes.faith)

	def score_dfn(self, p):
		return 4 + math.ceil(3.5*p.attributes.faith) + math.ceil(3.5*p.attributes.strength)

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

		

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Paladin"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_sealing(amt=3)
		self.msg += f"{self.attacker.name} casts a prayer on their blade to seal their foes."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_attdown(amt=2)
			self.defender.stack_evadown(amt=2)
			self.defender.stack_defdown(amt=2)
			self.defender.stack_accdown(amt=2)

			self.msg += f"{self.attacker.name} has weakened {self.defender.name} with a holy censure."
		else:
			self.msg += f"{self.defender.name} maintains their conviction against {self.attacker.name}'s censure."