from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

class Cryomancer(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.intelligence) + math.ceil(0.75*p.faith) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(0.75*p.level) + 2

	def score_att(self, p):
		return 3*p.faith+3*p.intelligence

	def score_def(self, p):
		return 3 + 2*(p.faith + p.intelligence)

	def basic_action(self, u, players, npcs):
		targets = random.choices(npcs, k=3*(1 + len(npcs)//10))

		for t in targets:
			t.stack_defdown()
			t.stack_attdown()

		print(f"{u.name} conjures a frozen fog that chills their foes, lowering their defense and attack.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		if utils.compute_hit(u, target):
			target.stack_stun(amt=random.randint(1, 4))
			print(f"{u.name} has frozen {target.label} solid.")
		else:
			print(f"{u.name} has failed to freeze {target.label}")

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]