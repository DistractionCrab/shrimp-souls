from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

class Assassin(ClassSpec):
	def max_hp(self, p):
		return 10 + 1 * p.level + 4*p.attributes.vigor

	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return 12 + math.ceil(1.25*p.attributes.dexterity) + math.ceil(1.25*p.attributes.faith)

	def score_att(self, p):
		return math.ceil(2.5*p.attributes.faith + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return p.level + 2*p.attributes.dexterity

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
		return "Assassin"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_invis(amt=2)
		self.msg += f"{self.attacker.name} hides in the shadows."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_poison(amt=random.randint(1, 6))
			dmg = random.randint(1, 10)*(1 + (self.attacker.attributes.dexterity + self.attacker.attributes.luck)//10)
			dmg = dmg if self.attacker.invis == 0 else 2*dmg
			self.defender.damage(dmg)

			self.msg += f"{self.attacker.name}'s poisoned blade pierces {self.defender.name} dealing {dmg} damage."
		else:
			self.msg += f"{self.attacker.name}'s poisoned blade misses their target. "