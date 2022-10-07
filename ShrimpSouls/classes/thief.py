from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

STEAL_BONUS_THRESHOLD = 10

class Thief(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(p.level/2) + math.ceil(p.dexterity/2)

	def score_eva(self, p):
		return 10 + math.ceil(1.25 * p.luck) + math.ceil(p.dexterity*1.25)	

	def score_att(self, p):
		return math.ceil(3.5*p.dexterity + 2.5*p.luck)

	def score_def(self, p):
		return p.level + 2 * p.dexterity

	def basic_action(self, u, players, npcs):
		target = random.choices(npcs)[0]
		amt = sum(random.randint(1, 4) for i in range(1 + u.luck//STEAL_BONUS_THRESHOLD))
		msg = ''

		if bool(random.getrandbits(1)):
			u.add_shrimp(amt)
			msg += f"{u.name} manages to steal {amt} shrimp from {target.name}. "
			# See if you pilfer armor.
			if bool(random.getrandbits(1)):
				target.stack_defdown()
				u.stack_defup()
				msg += f"{u.name} pilfers armor from {target.name}. "

			if bool(random.getrandbits(1)):
				target.stack_attdown()
				u.stack_attup()
				msg += f"{u.name} pilfers the weapon from {target.name}. "
		else:
			msg += f"{u.name} failed to steal any shrimp. "		

		print(msg)

	def medium_action(self, u, players, npcs):
		pass

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		target = random.choices(opponents)[0]

		if super().compute_hit(actor, target):
			dmg = super().compute_dmg(actor, target)

			return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of their sword.")]