from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Warrior(ClassSpec):
	def score_eva(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.strength + 2.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return 2*p.level + p.attributes.strength + p.attributes.dexterity

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
		return "Warrior"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_attup(amt=3)
		self.msg += f"{self.attacker.name} sharpens their blade, increasing their attack."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender):
			dmg = 5 + random.randint(1, 6)*(1 + (self.attacker.attributes.strength + self.attacker.attributes.dexterity)//10)
			self.defender.use_defup(self.defender.defup)
			self.defender.use_evaup(self.defender.evaup)
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s breaks {self.defender.name}'s armor and deals {dmg} damage. "

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."