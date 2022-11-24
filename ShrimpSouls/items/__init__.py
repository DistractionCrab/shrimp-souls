import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
from dataclasses import dataclass

@dataclass
class Item:
	display: str = "Garbage"
	applicable: bool = False

	def act(self, p, targets, env):
		if self.applicable and len(targets) > 0:
			return self.apply(p, targets, env)
		else:
			return self.use(p, env)

	def use(self, p, env):
		return []

	def apply(self, p, targets, env):
		return []


@dataclass
class MinorHealingPotion(Item):
	display: str = "Minor Healing Potion"

	def use(self, p, env):
		return [actions.HealTarget(
			attacker=p,
			defender=p,
			score=utils.RawScore(s=ss.Scores.Vig))]