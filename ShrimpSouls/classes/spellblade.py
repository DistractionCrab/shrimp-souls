import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
import ShrimpSouls.actions as actions
from dataclasses import dataclass
import random
import math


def enchant(u, targets, env):		
	return [Action1(attacker=u,defender=u)]

def magic_cover(u, targets, env):
	t = env.find_valid_target(u, True, True, targets=targets, amt=1)
	if len(t) == 0:
		return []
	else:
		return [Target1(attacker=u, defender=t[0])]

@dataclass
class MagicGreatsword(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.DamageAction(
				attacker=u,
				defender=t,
				dmgtype=actions.DamageType.Magic,
				score_dmg=utils.ScoreDamage(m1=0.5))
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"enchant": enchant,
	"magic_cover": magic_cover,
	"magic_greatsword": MagicGreatsword(),
}

class SpellBlade(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP


	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=10, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, intelligence=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, strength=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, intelligence=1, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, intelligence=1, strength=1)



	def duel_action(self, actor, env):
		return [
			actions.DamageTarget(attacker=actor, defender=t) 
			for t in env.find_valid_target(actor, False, [ss.Positions.FRONT], True)]

	@property
	def cl_string(self):
		return "Spellblade"

@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnum.attup.stack(self.attacker, amt=5)
		ss.StatusEnum.defup.stack(self.attacker, amt=5)
		self.msg += f"{self.attacker.name} enchants their sword and shield, enhancing their attack and defense."


@dataclass
class Target1(actions.Action):
	def apply(self):
		ss.StatusEnum.block.stack(self.defender)
		ss.StatusEnum.soulmass.stack(self.defender)

		self.msg += f"{self.attacker.name} is covering {self.defender.name} with a magical defense."