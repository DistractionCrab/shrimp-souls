from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Swordsman(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.attributes.dexterity*0.65)

	def score_att(self, p):
		return math.ceil(2.5*p.attributes.strength + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return 2*p.level + p.attributes.strength + p.attributes.dexterity

	def basic_action(self, u, env):
		npcs = list(env.npcs)
		targets = random.sample(npcs, k=min(3, len(npcs)))

		return [Action1(attacker=u, defender=t) for t in targets]

		#print(f"{u.name} hamstrings some of their foes, decreasing their evasion.")

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Swordsman"

@dataclass
class Action1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_evadown(amt=2)
			self.msg += f"{self.attacker.name} has hamstrung {self.defender.name}. "
		else:
			self.msg += f"{self.attacker.name} has missed their hamstring. "

@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender):
			self.defender.stack_bleed(amt=random.randint(1, 2))
			self.msg += f"{self.attacker.name}'s sharp blades slice into {self.defender.name}. "
		else:
			self.msg += f"{self.attacker.name}'s blades miss {self.defender.name}. "
