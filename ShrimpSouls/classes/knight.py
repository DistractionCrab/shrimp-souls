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
		return 3*attributes.p.strength + 3*p.attributes.dexterity 

	def score_dfn(self, p):
		return p.attributes.strength + 4*p.attributes.dexterity + 5

	def basic_action(self, u, env):
		u.stack_block(amt=3)
		print(f"{u.name} readies their shield to block attacks.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		target.stack_block()
		u.stack_defdown()
		u.stack_attdown()

		print(f"{u.name} is covering {target.name}.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Knight"


		