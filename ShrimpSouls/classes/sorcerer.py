from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math

class Sorcerer(ClassSpec):
	def score_acc(self, p):
		return 10 + math.ceil(1.25*p.intelligence) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 4*p.intelligence +3

	def score_def(self, p):
		return math.ceil(p.level*1.25)

	def basic_action(self, u, party, opponents):
		u.stack_soulmass(amt=3)
		print(f"{u.name} summons a phalanx of soulmasses to defend themselves.")

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		act = actions.DamageTarget(
			attacker=u, 
			defender=target,
			dmgoverride=random.randint(1, 10)*(1 + int(u.intelligence/10)),
			dmgtype=actions.DamageType.Magic,
			abilityrange=actions.AbilityRange.Long)

		act.apply()
		print(act.msg)

	def ultimate_action(self, u):
		pass

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]