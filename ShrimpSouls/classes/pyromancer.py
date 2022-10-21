from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

class Pyromancer(ClassSpec):
	def max_hp(self, p):
		return 20 + 2*p.level + 4 * p.attributes.vigor

	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.attributes.intelligence) + math.ceil(0.75*p.attributes.faith) + math.ceil(0.25*p.attributes.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(1.25*p.level) + 2

	def score_att(self, p):
		return 3*p.attributes.faith+3*p.attributes.intelligence

	def score_dfn(self, p):
		return math.ceil(1.5*p.level) + 3

	def basic_action(self, u, env):
		npcs = list(n for n in env.npcs if not n.dead)
		targets = random.sample(npcs, k=min(3, len(npcs)))
		return [Action1(attacker=u,defender=t) for t in targets]
			

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]


	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Pyromancer"

@dataclass
class Action1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_burn(amt=3)
			self.msg += f"{self.attacker.name} has burned {self.defender.name} for 3 turns."
		else:
			self.msg += f"{self.attacker.name} failed to burn {self.defender.name}."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			dmg = random.randint(1, 10)*(1 + (self.attacker.attributes.faith + self.attacker.attributes.intelligence)//10)
			self.defender.stack_burn(amt=3)
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s Fireball strikes {self.defender.name} for {dmg} damage and burns them for 5 turns"

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."