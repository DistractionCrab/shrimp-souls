from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Knight(ClassSpec):
	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_att(self, p):
		return 3*p.strength + 3*p.dexterity 

	def score_def(self, p):
		return p.strength + 4*p.dexterity + 5 if p.block > 0 else 0

	def basic_action(self, u, players, npcs):
		u.stack_block(amt=3)
		print(f"{u.name} readies their shield to block attacks.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		target.stack_block()
		u.stack_defdown()
		u.stack_attdown()

		print(f"{u.name} is covering {target.label}.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]


		