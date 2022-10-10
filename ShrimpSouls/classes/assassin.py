from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

class Assassin(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.dexterity/2)

	def score_eva(self, p):
		return 12 + math.ceil(1.25*p.dexterity) + math.ceil(1.25*p.faith)

	def score_att(self, p):
		return math.ceil(2.5*p.faith + 3.5*p.dexterity)

	def score_def(self, p):
		return p.level + 2*p.dexterity

	def basic_action(self, u, players, npcs):
		u.stack_invis()
		print(f"{u.name} hides in the shadows.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)
		if utils.compute_hit(u, target):
			target.stack_poison(amt=random.randint(1, 6))
			print(f"{u.name}'s poisoned blade pierces {target.label}.")
		else:
			print(f"{u.name}'s poisoned blade misses their target.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]