from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

BONUS_THRESHOLD = 10

class Juggernaut(ClassSpec):
	def score_eva(self, p):
		return super().score_eva(p) - 2

	def score_acc(self, p):
		return super().score_acc(p)

	def score_att(self, p):
		return 4*p.attributes.strength 

	def score_dfn(self, p):
		return 4*p.attributes.strength + 4

	def basic_action(self, u, env):
		players = env.players
		npcs = env.npcs
		targets = random.choices(players, k=3*(1 + len(players)//10))

		for t in targets:
			t.stack_attup(amt=2)

		print(f"{u.name} emits a powerful warcry, bolstering some of their party.")

	def targeted_action(self, u, target, env):
		target = env.get_target(target)

		if utils.compute_hit(u, target):
			target.stack_defdown(random.randint(1, 6))
			print(f"{u.name} has shattered {target.name}'s armor. ")
			act = actions.DamageTarget(
				attacker=u, 
				defender=target,
				dmgoverride=random.randint(1, 10)*(1 + (u.strength)//10),
				dmgtype=actions.DamageType.Slash,
				abilityrange=actions.AbilityRange.Close)
			act.apply()
			print(act.msg)
		else:
			print(f"{u.name} missed with their armor shatter.")



	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Juggernaut"