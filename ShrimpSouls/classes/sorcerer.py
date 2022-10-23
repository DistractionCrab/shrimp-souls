from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

class Sorcerer(ClassSpec):
	@property
	def position(self):
		return ss.Positions.BACK
		
	def max_hp(self, p):
		return 20 + 2 * p.level + 4 * p.attributes.vigor

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

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

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
		if utils.compute_hit(self.attacker, self.defender)[0]:
			dmg = random.randint(5, 15)*(1 + 2*(self.attacker.attributes.intelligence//10))
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s Souls Spear strikes {self.defender.name} for {dmg} damage."

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."