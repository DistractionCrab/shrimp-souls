from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Paladin(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p)

	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_att(self, p):
		return math.ceil(3*p.strength) + math.ceil(4*p.faith)

	def score_def(self, p):
		return 4 + math.ceil(3.5*p.faith) + math.ceil(3.5*p.strength)

	def basic_action(self, u, players, npcs):
		u.stack_sealing(amt=3)
		print(f"{u.name} casts a prayer on their blade to seal their foes.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		if utils.compute_hit(u, target):
			target.stack_attdown(amt=2)
			target.stack_evadown(amt=2)
			target.stack_defdown(amt=2)
			target.stack_accdown(amt=2)

			print(f"{u.name} has weakened {target.label} with a holy censure.")
		else:
			print(f"{target.label} maintains their conviction against {u.name}'s censure.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]