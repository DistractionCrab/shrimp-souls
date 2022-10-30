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
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
		
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=4, vigor=2)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, intelligence=1, faith=1, dexterity=0.25)

	def score_eva(self, p):
		return cs.stat_map(p, base=10, faith=0.75, dexterity=0.25)

	def score_att(self, p):
		return cs.stat_map(p, faith=3, intelligence=3)

	def score_dfn(self, p):
		return cs.stat_map(p, base=3, faith=3.5, intelligence=3.5)

	def basic_action(self, u, env):
		npcs = list(n for n in env.npcs if not n.dead)
		targets = random.sample(npcs, k=min(3, len(npcs)))

		return [Action1(attacker=u, defender=t) for t in targets]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

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
		return "Cryomancer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_evadown(amt=2)
		self.defender.stack_attdown(amt=2)

		self.msg += f"{self.attacker.name} chills {self.defender.name} lowering attack and defense."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			amt = random.randint(1, 4)
			self.defender.stack_stun(amt=amt)
			self.msg += f"{self.attacker.name} has frozen {self.defender.name} solid for {amt} turns."
		else:
			self.msg += f"{self.attacker.name} has failed to freeze {self.defender.name}"