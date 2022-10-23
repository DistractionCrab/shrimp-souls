import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

class Bard(ClassSpec):
	@property
	def position(self):
		return ss.Positions.BACK
	
	def max_hp(self, p):
		return 20 + 2*p.level + 5*p.attributes.vigor

	def score_acc(self, p):
		return super().score_acc(p) + 2

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.attributes.dexterity*0.65)

	def score_att(self, p):
		return p.attributes.dexterity + p.attributes.intelligence + p.attributes.perception + p.attributes.luck

	def score_dfn(self, p):
		return math.ceil(1.5*p.level) + 3

	def basic_action(self, u, env):
		players = list(n for n in env.players if not n.dead)
		targets = random.choices(players, k=min(3, len(players)))

		return [Action1(attacker=u, defender=t) for t in targets]

		

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
		return "Bard"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_encourage(amt=3)
		self.msg += f"{self.attacker.name}'s ballad encourages {self.defender.name}."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if self.defender.is_player:
			self.defender.use_charm(amt=1)
			print(f"{self.attacker.name} has weakened the charm magic on {self.defender.name}.")
		elif self.defender.is_npc:
			if utils.compute_hit(self.attacker, self.defender)[0]:
				t = random.randint(1,4)
				self.defender.stack_charm(amt=t)
				self.msg += f"{self.attacker.name} has charmed {self.defender.name} for {t} turns."
			else:
				self.msg += f"{self.attacker.name} failed to charm {self.defender.name}."