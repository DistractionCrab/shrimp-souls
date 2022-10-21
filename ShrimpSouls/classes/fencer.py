from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Fencer(ClassSpec):
	def max_hp(self, p):
		return 20 + 2*p.level + 5*p.attributes.vigor

	def score_acc(self, p):
		return 12 + math.ceil(1.5*p.attributes.dexterity)

	def score_eva(self, p):
		return 12 + math.ceil(1.5*p.attributes.dexterity)

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return p.level + 2*p.attributes.dexterity

	def basic_action(self, u, env):
		return [Action1(attacker=u,defender=u)]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]



	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Fencer"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_ripstance(amt=2)
		self.msg += f"{self.attacker.name} has entered a riposting stance."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.taunt_target(self.attacker)
			self.msg += f"{self.attacker.name} has taunted {self.defender.name} into attacking them. "
		else:
			self.msg += f"{self.attacker.name} has failed to taunt {self.defender.name}. "