import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def encourage(u, targets, env):
	targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]


def charm(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for charming.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"encourage": encourage,
	"charm": charm,
}

class Bard(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	@property
	def position(self):
		return ss.Positions.BACK
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=2, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, base=12, level=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=0.35, dexterity=0.65)

	def score_att(self, p):
		return cs.stat_map(p, dexterity=1, intelligence=1, luck=1, perception=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=1.5, base=3)

	def basic_action(self, u, env):
		players = list(n for n in env.players if not n.dead)
		targets = random.choices(players, k=min(3, len(players)))

		return [Action1(attacker=u, defender=t) for t in targets]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]
		

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