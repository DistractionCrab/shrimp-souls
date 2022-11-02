import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

def chill(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def freeze(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for freezing.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"chill": chill,
	"freeze": freeze,
}

class Cryomancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	def max_hp(self, p):
		return cs.stat_map(p, base=100, level=20, vigor=10)

	def score_acc(self, p):
		return cs.stat_map(p, level=27, intelligence=5, faith=5)

	def score_eva(self, p):
		return cs.stat_map(p, level=25)

	def score_att(self, p):
		return cs.stat_map(p, level=22, faith=4, intelligence=4)

	def score_dfn(self, p):
		return cs.stat_map(p, level=35, intelligence=8, faith=8)

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Cryomancer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_evadown(amt=2)
		self.defender.stack_attdown(amt=2)

		self.msg += f"{self.attacker.name} chills {self.defender.name} lowering attack and defense."


@dataclass
class Target1(actions.EffectAction):
	def on_hit(self):
		amt = random.randint(1, 4)
		self.defender.stack_stun(amt=amt)
		self.msg += f"{self.attacker.name} has frozen {self.defender.name} solid for {amt} turns."

	def on_miss(self):
		self.msg += f"{self.attacker.name} has failed to freeze {self.defender.name}"