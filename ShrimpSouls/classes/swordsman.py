from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

class Swordsman(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.attributes.dexterity*0.65)

	def score_att(self, p):
		return math.ceil(2.5*p.attributes.strength + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return 2*p.level + p.attributes.strength + p.attributes.dexterity

	def basic_action(self, u, env):
		players = env.players
		npcs = env.npcs
		targets = random.choices(npcs, k=2*(1 + len(npcs)//10))

		for t in targets:
			t.stack_evadown(amt=2)

		print(f"{u.name} hamstrings some of their foes, decreasing their evasion.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)
		if utils.compute_hit(u, target):
			target.stack_bleed(amt=random.randint(1, 2))
			print(f"{u.name}'s sharp blades slice into {target.name}.")
		else:
			print(f"{u.name}'s blades miss {target.name}.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Swordsman"