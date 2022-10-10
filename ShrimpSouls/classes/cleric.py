from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Cleric(ClassSpec):
	def score_acc(self, p):
		return super().score_acc(p) + 1

	def score_eva(self, p):
		return super().score_eva(p) - 1

	def score_att(self, p):
		return 3*p.strength+3*p.faith

	def score_def(self, p):
		return 2*p.strength + 3*p.faith

	def basic_action(self, u, players, npcs):
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_defup(amt=2)

		print(f"{u.name} utters a short prayer, bolstering some of their party's defense.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)
		target.use_burn(target.burn)
		target.use_attdown(target.attdown)
		target.use_evadown(target.evadown)
		target.use_accdown(target.accdown)
		target.use_defdown(target.defdown)
		target.use_poison(target.poison)
		target.use_stun(target.stun)

		print(f"{u.name} has cleansed {target.label} of their debuffs.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]
