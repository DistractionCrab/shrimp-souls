from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math
import ShrimpSouls.utils as utils

class Cryomancer(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(0.75*p.attributes.intelligence) + math.ceil(0.75*p.attributes.faith) + math.ceil(0.25*p.attributes.dexterity)

	def score_eva(self, p):
		return 10 + math.ceil(0.75*p.level) + 2

	def score_att(self, p):
		return 3*p.attributes.faith+3*p.attributes.intelligence

	def score_dfn(self, p):
		return 3 + 2*(p.attributes.faith + p.attributes.intelligence)

	def basic_action(self, u, env):
		npcs = list(n for n in npcs if not n.dead)
		targets = random.choices(npcs, k=3*(1 + len(npcs)//10))

		for t in targets:
			t.stack_defdown()
			t.stack_attdown()

		print(f"{u.name} conjures a frozen fog that chills their foes, lowering their defense and attack.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		if utils.compute_hit(u, target):
			target.stack_stun(amt=random.randint(1, 4))
			print(f"{u.name} has frozen {target.name} solid.")
		else:
			print(f"{u.name} has failed to freeze {target.name}")

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Cryomancer"