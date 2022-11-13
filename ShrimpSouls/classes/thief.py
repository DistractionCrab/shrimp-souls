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
	return [Action1(attacker=u, defender=r) for r in t]


def poach(u, targets, env):
	if len(targets) == 0:
		t = env.find_valid_target(u, False, [ss.Positions.FRONT], True)
		if len(t) == 0:
			return [actions.Error(info="No targets could be found...")]
		t = t[0]
	else:
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
		return cs.stat_map(p, base=100, level=10, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, level=11, dexterity=1, luck=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1, luck=1)

	def score_att(self, p):
		return cs.stat_map(p, level=11, dexterity=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=9, vigor=1)


	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

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
