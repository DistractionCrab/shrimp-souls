from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class SpellBlade(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_att(self, p):
		return 3*p.attributes.strength+3*p.attributes.intelligence

	def score_dfn(self, p):
		return 2*p.attributes.strength + 3*p.attributes.intelligence

	def basic_action(self, u, env):
		u.stack_attup()
		u.stack_defup()
		print(f"{u.name} enchants their sword and shield enhancing their attack and defense.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		target.stack_block()
		target.stack_soulmass()
		u.stack_defdown()
		u.stack_evadown()
		u.stack_accdown()

		print(f"{u.name} is covering {target.name} with a magical defense.")

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Spellblade"