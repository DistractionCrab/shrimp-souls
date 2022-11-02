from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def pyroclasm(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def fireball(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"pyroclasm": pyroclasm,
	"fireball": fireball,
}

class Pyromancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base = 100, level=10, vigor=20)

	@property
	def position(self):
		return ss.Positions.BACK

	def score_acc(self, p):
		return cs.stat_map(p, level=25, intelligence=5, faith=2)

	def score_eva(self, p):
		return cs.stat_map(p, level=27, intelligence=2, faith=5)

	def score_att(self, p):
		return cs.stat_map(p, level=30, intelligence=10, faith=10)

	def score_dfn(self, p):
		return cs.stat_map(p, level=22)

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Pyromancer"

@dataclass
class Action1(actions.EffectAction):
	def on_hit(self):
		t = random.randint(1, 3)
		self.defender.stack_burn(amt=t)
		self.msg += f"{self.attacker.name} has burned {self.defender.name} for {t} turns."

	def on_miss(self):
		self.msg += f"{self.attacker.name} failed to burn {self.defender.name}."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.3)
	statuses: tuple = ((ss.StatusEnum.burn, 2),)