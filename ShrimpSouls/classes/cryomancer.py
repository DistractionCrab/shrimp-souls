from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

class Cryomancer(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.attributes.intelligence) + math.ceil(0.75*p.attributes.faith) + math.ceil(0.25*p.attributes.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(0.75*p.level) + 2

	def score_att(self, p):
		return 3*p.attributes.faith+3*p.attributes.intelligence

	def score_dfn(self, p):
		return 3 + 2*(p.attributes.faith + p.attributes.intelligence)

	def basic_action(self, u, env):
		npcs = list(n for n in env.npcs if not n.dead)
		targets = random.sample(npcs, k=min(3, len(npcs)))

		return [Action1(attacker=u, defender=t) for t in targets]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

		

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Cryomancer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_defdown(amt=2)
		self.defender.stack_attdown(amt=2)

		self.msg += f"{self.attacker.name} chills {self.defender.name} lowering attack and defense."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender):
			self.defender.stack_stun(amt=random.randint(1, 4))
			self.msg += f"{self.attacker.name} has frozen {self.defender.name} solid."
		else:
			print(f"{self.attacker.name} has failed to freeze {self.defender.name}")