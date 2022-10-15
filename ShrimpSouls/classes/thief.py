from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

STEAL_BONUS_THRESHOLD = 10

class Thief(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(1.25 * p.attributes.luck) + math.ceil(p.attributes.dexterity*1.25)	

	def score_att(self, p):
		return math.ceil(3.5*p.attributes.dexterity + 2.5*p.attributes.luck)

	def score_dfn(self, p):
		return p.level + 2 * p.attributes.dexterity

	def basic_action(self, u, env):
		players = env.players
		npcs = env.npcs
		target = random.choices(npcs)[0]
		amt = sum(random.randint(1, 4) for i in range(1 + u.luck//STEAL_BONUS_THRESHOLD))
		msg = ''

		if utils.compute_hit(u, target):
			u.add_shrimp(amt)
			msg += f"{u.name} manages to steal {amt} shrimp from {target.name}. "
			# See if you pilfer armor.
			if utils.compute_hit(u, target):
				target.stack_defdown()
				u.stack_defup()
				msg += f"{u.name} pilfers armor from {target.name}. "

			if utils.compute_hit(u, target):
				target.stack_attdown()
				u.stack_attup()
				msg += f"{u.name} pilfers the weapon from {target.name}. "
		else:
			msg += f"{u.name} failed to steal any shrimp. "		

		print(msg)

	def targeted_action(self, u, target, env):
		target = env.get_npc(target)

		if (target.hp/target.max_hp) < 0.2:
			if utils.compute_hit(u, target):
				target.damage(-target.hp)
				u.add_shrimp(2*target.xp)
				print(f"{u.name} managed to poach {target.name} and earned {2*target.xp} shrimp.")
			else:
				print(f"{u.name} failed to poach {target.name}.")

		else:
			print(f"{target.name} is not weak enough for {u.name} to poach.")
		

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	@property
	def cl_string(self):
		return "Thief"