from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

class Sorcerer(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(1.25*p.attributes.intelligence) + math.ceil(0.25*p.attributes.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 4*p.attributes.intelligence + 3

	def score_dfn(self, p):
		return math.ceil(p.level*1.25) + math.ceil(p.attributes.intelligence * 2.25)

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):

		return [Target1(attacker=u, defender=target)]

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Sorcerer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_soulmass(amt=2)
		self.msg += f"{self.attacker.name} summons a phalanx of soulmasses to defend themselves."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender):
			dmg = random.randint(5, 15)*(1 + 2*(self.attacker.attributes.intelligence//10))
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s Souls Spear strikes {self.defender.name} for {dmg} damage."

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."