import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

def invis(u, targets, env):
	return [Action1(attacker=u, defender=u)]

def poison_blade(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poison blade.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"invis": invis,
	"poison_blade": poison_blade,
}

class Assassin(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base=10, level=1, vigor=4)

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=1, dexterity=0.5)

	def score_eva(self, p):
		return cs.stat_map(p, base=12, dexterity=1.25, faith=1.25)

	def score_att(self, p):
		return cs.stat_map(p, faith=2.5, dexterity=3.5)
		return math.ceil(2.5*p.attributes.faith + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return cs.stat_map(p, level=1, dexterity=2)
		return p.level + 2*p.attributes.dexterity

	def basic_action(self, u, env):
		return [Action1(attacker=u, defender=u)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

	@property
	def cl_string(self):
		return "Assassin"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.attacker.stack_invis(amt=2)
		self.msg += f"{self.attacker.name} hides in the shadows."


@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_poison(amt=random.randint(1, 6))
			dmg = random.randint(1, 10)*(1 + (self.attacker.attributes.dexterity + self.attacker.attributes.luck)//10)
			dmg = dmg if self.attacker.invis == 0 else 2*dmg
			
			self.defender.damage(dmg)

			self.msg += f"{self.attacker.name}'s poisoned blade pierces {self.defender.name} dealing {dmg} damage."
		else:
			self.msg += f"{self.attacker.name}'s poisoned blade misses their target. "

		self.attacker.use_invis(self.attacker.invis)