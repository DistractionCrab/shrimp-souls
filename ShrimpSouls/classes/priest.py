import ShrimpSouls as ss
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
import random
import math


HEAL_DICE_THRESHOLD = 10

class Priest(ClassSpec):
	def score_acc(self, p):
		return  10 + math.ceil(1.25*p.intelligence) + math.ceil(0.25*p.dexterity)

	def score_eva(self, p):
		return 12 + p.level

	def score_att(self, p):
		return 2*p.faith

	def score_def(self, p):
		return math.ceil(p.level*1.25)

	def basic_action(self, u, players, npcs):
		targets = list(filter(lambda x: not x.dead, players))
		targets = set(random.choices(
			targets, 
			k=3*(1 + len(targets)//10),
			weights=[1/(1 + p.health) for p in targets]))
		targets = list(filter(lambda x: not x.dead, targets))

		for t in targets:
			t.damage(-(random.randint(1, 4)*(1 + u.faith//HEAL_DICE_THRESHOLD)))

		print(f"{u.name} has healed {', '.join(t.name for t in targets)}.")

		

	def targeted_action(self, u, target, env):
		target = env.get_labeled(target)

		if target.dead:
			target.damage(-target.max_health)
			print(f"{u.name} has revived {target.label} from the dead.")
		else:
			amt = random.randint(10, 20)*(1 + u.faith//HEAL_DICE_THRESHOLD)
			target.damage(-amt)

			print(f"{u.name} has healed {target.label} for {amt} hp.")

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, party, opponents):
		if sum(p.health/p.max_health for p in party)/len(party) < 0.5:
			party = filter(lambda x: not x.dead, party)
			heal = sum(random.randint(1, 4)  for _ in range((1 + actor.faith//HEAL_DICE_THRESHOLD)))
			target = min(party, key=lambda p: p.health)
			return [actions.HealTarget(attacker=actor, defender=target, dmg=heal)]
		else:			
			target = self.find_valid_target(opponents)
			return [actions.DamageTarget(attacker=actor, defender=target)]
