import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import random
import math

def warcry(u, targets, env):
	targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)
	return [Action1(attacker=u, defender=t) for t in targets]

def shatter(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for shattering.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"warcry": warcry,
	"shatter": shatter,
}

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=7)

	def score_eva(self, p):
		return cs.stat_map(p, base=8, level=1)

	def score_acc(self, p):
		return cs.stat_map(p, level=1, base=10)

	def score_att(self, p):
		return cs.stat_map(p, strength=4)

	def score_dfn(self, p):
		return cs.stat_map(p, base=4, strength=4)

	def basic_action(self, u, env):
		targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)

		return [Action1(attacker=u, defender=t) for t in targets]

	def targeted_action(self, u, target, env):

		return [Target1(attacker=u, defender=target)]


	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]



	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

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