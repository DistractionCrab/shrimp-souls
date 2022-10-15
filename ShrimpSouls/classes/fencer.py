from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Fencer(ClassSpec):
	def score_acc(self, p):
		return 12 + math.ceil(1.5*p.attributes.dexterity)

	def score_eva(self, p):
		return 12 + math.ceil(1.5*p.attributes.dexterity)

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return p.level + 2*p.attributes.dexterity

	def basic_action(self, u, env):
		u.stack_ripstance()
		print(f"{u.name} has entered a riposting stance.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		if utils.compute_hit(u, target):
			target.taunt_target(u)
			print(f"{u.name} has taunted {target.name} into attacking them.")
		else:
			print(f"{u.name} has failed to taunt {target.name}.")


	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Fencer"