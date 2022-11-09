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
		t = env.find_valid_target(u, False, ss.Positions, True)
		if t is None:
			return [actions.Error(info="No targets could be found...")]
	else:
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
		return cs.stat_map(p, base=100, level=7, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, perception=2, dexterity=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, perception=1, dexterity=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, perception=1)


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
class Target1(actions.EffectAction):

	def on_hit(self):
		if self.defender.immune(ss.StatusEnum.charm):
			self.msg += f"{self.defender.name} is immune to being charmed."
		elif self.defender.is_player:
			self.defender.use_charm(amt=1)
			print(f"{self.attacker.name} has weakened the charm magic on {self.defender.name}.")
		elif self.defender.is_npc:
			t = random.randint(1,4)
			self.defender.stack_charm(amt=t)
			self.msg += f"{self.attacker.name} has charmed {self.defender.name} for {t} turns."
			
	def on_miss(self):
		self.msg += f"{self.attacker.name} failed to charm {self.defender.name}."