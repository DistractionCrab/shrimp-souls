import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

STEAL_BONUS_THRESHOLD = 10

def steal(u, targets, env):
	t = env.find_valid_target(u, False, ss.Positions, True)
	if t is None:
		return []
	else:
		return [Action1(attacker=u, defender=t)]

def poach(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"steal": steal,
	"poach": poach,
}

class Thief(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP	

	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=2, vigor=5)
		return 20 + 2 * p.level + 5*p.attributes.vigor

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=0.5, dexterity=0.5)
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return cs.stat_map(p, base=10, luck=1.25, dexterity=1.5)

	def score_att(self, p):
		return cs.stat_map(p, dexterity=3.5, luck=2.5)
		return math.ceil(3.5*p.attributes.dexterity + 2.5*p.attributes.luck)

	def score_dfn(self, p):
		return cs.stat_map(p, level=1, dexterity=2)
		return p.level + 2 * p.attributes.dexterity


	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Thief"


@dataclass
class Action1(actions.Action):
	def apply(self):
		amt = sum(random.randint(1, 4) for i in range(1 + self.attacker.attributes.luck//STEAL_BONUS_THRESHOLD))
		if utils.compute_bool(self.attacker, self.defender):
			self.attacker.add_shrimp(amt)
			self.msg += f"{self.attacker.name} manages to steal {amt} shrimp from {self.defender.name}. "
			# See if you pilfer armor.
			if utils.compute_bool(self.attacker, self.defender):
				self.defender.stack_defdown()
				self.attacker.stack_defup()
				self.msg += f"{self.attacker.name} pilfers armor from {self.defender.name}. "

			if utils.compute_bool(self.attacker, self.defender):
				self.defender.stack_attdown()
				self.attacker.stack_attup()
				self.msg += f"{self.attacker.name} pilfers the weapon from {self.defender.name}. "
		else:
			self.msg += f"{self.attacker.name} failed to steal any shrimp. "

		return self.msg

@dataclass
class Target1(actions.Action):
	def apply(self):
		if self.defender.is_player:
			self.msg += f"{self.attacker.name} cannot poach friendly players, naughty thief."
			return
		if self.defender.dead:
			self.msg += f"{self.attacker.name} cannot poach an enemy while their target is dead."
			return
		if (self.defender.hp/self.defender.max_hp) < 0.2:
			if utils.compute_bool(self.attacker, self.defender):
				self.defender.damage(self.defender.max_hp)
				self.attacker.add_shrimp(self.defender.xp)
				self.msg += f"{self.attacker.name} managed to poach {self.defender.name} and earned {self.defender.xp} shrimp."
			else:
				self.msg += f"{self.attacker.name} failed to poach {self.defender.name}."

		else:
			self.msg += f"{self.defender.name} is not weak enough for {self.attacker.name} to poach."
