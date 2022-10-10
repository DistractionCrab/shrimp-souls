from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Bard(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 2

	def score_eva(self, p):
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.dexterity*0.65)

	def score_att(self, p):
		return p.dexterity + p.intelligence + p.perception + p.luck

	def score_def(self, p):
		return math.ceil(1.5*p.level) + 3

	def basic_action(self, u, players, npcs):
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_encourage()

		print(f"{u.name} plays a wartime ballad, encouraging some of their party.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		if target.is_player:
			target.use_charm(amt=1)
			print(f"{u.name} has weakened the charm magic on {target.name}.")
		elif target.is_npc:
			t = random.randint(1,4)
			target.stack_charm(amt=t)
			print(f"{u.name} has charmed {target.label} for {t} turns.")
		

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]