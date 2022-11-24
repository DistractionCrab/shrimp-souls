import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def encourage(u, targets, env):
	t = env.find_valid_target(u, True, True, amt=3, targets=targets)
	return [Action1(attacker=u, defender=r) for r in t]


def charm(u, targets, env):
	t = env.find_valid_target(u, False, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

@dataclass
class Inspire(cs.Ability):
	t_amt: int = 3
	allyq: bool = True

	def act(self, u, targets, env):
		return [
			actions.StatusAction(
				attacker=u,
				defender=t,
				statuses={
					ss.StatusEnum.accup: lambda: 3,
					ss.StatusEnum.evaup: lambda: 3,
				},
				ignore_res=True)
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"encourage": encourage,
	"charm": charm,
	"inspire": Inspire(),
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
		return cs.stat_map(p, mult=5, base=100, level=7, vigor=3)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, perception=2, dexterity=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, perception=1, dexterity=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, perception=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Bard"


@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnnum.encourage(self.defender, amt=3)
		self.msg += f"{self.attacker.name}'s ballad encourages {self.defender.name}."


@dataclass
class Target1(actions.EffectAction):

	def on_hit(self):
		if self.defender.immune(ss.StatusEnum.charm):
			self.msg += f"{self.defender.name} is immune to being charmed."
		elif self.defender.is_player:
			ss.StatusEnnum.charm.use(self.defender, amt=1)
			print(f"{self.attacker.name} has weakened the charm magic on {self.defender.name}.")
		elif self.defender.is_npc:
			t = random.randint(1,4)
			ss.StatusEnnum.charm.stack(self.defender, amt=t)
			self.msg += f"{self.attacker.name} has charmed {self.defender.name} for {t} turns."
			
	def on_miss(self):
		self.msg += f"{self.attacker.name} failed to charm {self.defender.name}."