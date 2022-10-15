from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Warrior(ClassSpec):
	def score_eva(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.strength + 2.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return 2*p.level + p.attributes.strength + p.attributes.dexterity

	def basic_action(self, u, env):
		u.stack_attup(amt=4)
		print(f"{u.name} sharpens their axe, increasing their attack.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		if utils.compute_hit(u, target):
			target.use_defup(target.defup)
			target.use_evaup(target.evaup)
			print(f"{u.name} has broken {target.name}'s armor and removed their defense bonuses.")
			act = actions.DamageTarget(
				attacker=u, 
				defender=target,
				dmgoverride=random.randint(1, 4)*(1 + (u.strength + u.dexterity)//10),
				dmgtype=actions.DamageType.Slash,
				abilityrange=actions.AbilityRange.Close)
			act.apply()
			print(act.msg)
		else:
			print(f"{u.name} missed with their armor break.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Warrior"