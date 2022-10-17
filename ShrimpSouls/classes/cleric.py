from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math

class Cleric(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_att(self, p):
		return 3*p.attributes.strength+3*p.attributes.faith

	def score_dfn(self, p):
		return 2*p.attributes.strength + 3*p.attributes.faith

	def basic_action(self, u, env):
		players = list(p for p in env.players if not p.dead)
		targets = random.sample(players, k=min(3, len(players)))

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
		return "Cleric"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_defup(amt=3)
		self.msg += f"{self.attacker.name} prayer bolster's {self.defender.name}'s defense. "


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.use_burn(self.defender.burn)
		self.defender.use_attdown(self.defender.attdown)
		self.defender.use_evadown(self.defender.evadown)
		self.defender.use_accdown(self.defender.accdown)
		self.defender.use_defdown(self.defender.defdown)
		self.defender.use_poison(self.defender.poison)
		self.defender.use_stun(self.defender.stun)

		self.msg += f"{self.attacker.name} has cleansed {self.defender.name} of their debuffs."