from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import random
import math

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	def max_hp(self, p):
		return 20 + 5*p.level + 7*p.attributes.vigor

	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_acc(self, p):
		return super().score_acc(p)

	def score_att(self, p):
		return 4*p.attributes.strength 

	def score_dfn(self, p):
		return 4*p.attributes.strength + 4

	def basic_action(self, u, env):
		npcs = list(env.players)
		targets = random.sample(npcs, k=min(3, len(npcs)))

		return [Action1(attacker=u, defender=t) for t in targets]

	def targeted_action(self, u, target, env):

		return [Target1(attacker=u, defender=target)]



	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Juggernaut"

@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_attup(amt=3)
		self.msg += f"{self.attacker.name} warcry boosts {self.defender.name}'s attack."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			dmg = 5 + random.randint(1, 10)*(1 + 2*(self.attacker.attributes.strength//10))
			self.defender.stack_defdown(amt=3)
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s shatters {self.defender.name}'s armor and deals {dmg} damage. "

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."