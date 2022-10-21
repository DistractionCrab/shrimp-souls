from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

STEAL_BONUS_THRESHOLD = 10

class Thief(ClassSpec):
	def max_hp(self, p):
		return 20 + 2 * p.level + 5*p.attributes.vigor

	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(1.25 * p.attributes.luck) + math.ceil(p.attributes.dexterity*1.25)	

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.dexterity + 2.5*p.attributes.luck)

	def score_dfn(self, p):
		return p.level + 2 * p.attributes.dexterity

	def basic_action(self, u, env):
		enemies = list(env.npcs)
		
		if len(enemies) == 0:
			return []
		else:
			#print(enemies)
			target = random.sample(enemies,k=1)[0]
			return [Action1(attacker=u, defender = target)]
		

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]
		
		
	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Thief"


@dataclass
class Action1(actions.Action):
	def apply(self):
		amt = sum(random.randint(1, 4) for i in range(1 + self.attacker.attributes.luck//STEAL_BONUS_THRESHOLD))
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.attacker.add_shrimp(amt)
			self.msg += f"{self.attacker.name} manages to steal {amt} shrimp from {self.defender.name}. "
			# See if you pilfer armor.
			if utils.compute_hit(self.attacker, self.defender)[0]:
				self.defender.stack_defdown()
				self.attacker.stack_defup()
				self.msg += f"{self.attacker.name} pilfers armor from {self.defender.name}. "

			if utils.compute_hit(self.attacker, self.defender)[0]:
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
			if utils.compute_hit(self.attacker, self.defender)[0]:
				self.defender.damage(self.defender.max_hp)
				self.attacker.add_shrimp(self.defender.xp)
				self.msg += f"{self.attacker.name} managed to poach {self.defender.name} and earned {self.defender.xp} shrimp."
			else:
				self.msg += f"{self.attacker.name} failed to poach {self.defender.name}."

		else:
			self.msg += f"{self.defender.name} is not weak enough for {self.attacker.name} to poach."
