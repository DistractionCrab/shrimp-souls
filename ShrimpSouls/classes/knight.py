from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import random
import math

class Knight(ClassSpec):
	def max_hp(self, p):
		return 20 + 5*p.level + 6*p.attributes.vigor

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_att(self, p):
		return 3*p.attributes.strength + 3*p.attributes.dexterity 

	def score_dfn(self, p):
		return p.attributes.strength + 4*p.attributes.dexterity + 5

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

		

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Knight"


		
@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_block(amt=3)
		self.msg += f"{self.attacker.name} readies their shield to block attacks."


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.stack_block()
		self.attacker.stack_defdown()
		self.attacker.stack_attdown()

		self.msg += f"{self.attacker.name} is covering {self.defender.name}."