from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def soulmass(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def soulspear(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_enemy(targets[0])
	return [Target1(attacker=u, defender=target)]

ABI_MAP = {
	"soulmass": soulmass,
	"soulspear": soulspear,
}


class Sorcerer(ClassSpec):
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
		
	@property
	def position(self):
		return ss.Positions.BACK
		
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=2, vigor=4)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, intelligence=1.25, dexterity=0.25)

	def score_eva(self, p):
		return cs.stat_map(p, base=12, level=1)

	def score_att(self, p):
		return cs.stat_map(p, base=3, intelligence=4)

	def score_dfn(self, p):
		return cs.stat_map(p, level=1.25, intelligence=2.25)

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def ultimate_action(self, u):
		pass

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Sorcerer"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_soulmass(amt=2)
		self.msg += f"{self.attacker.name} summons a phalanx of soulmasses to defend themselves."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			dmg = random.randint(5, 15)*(1 + 2*(self.attacker.attributes.intelligence//10))
			self.defender.damage(dmg)
			self.msg += f"{self.attacker.name}'s Souls Spear strikes {self.defender.name} for {dmg} damage."

		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."