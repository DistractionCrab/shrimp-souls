import ShrimpSouls as ss
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
from dataclasses import dataclass

@dataclass
class Item:
	display: str = "Garbage"
	applicable: bool = False
	uses: int = 1

	def act(self, p, targets, env):
		if self.applicable and len(targets) > 0:
			v = self.apply(p, targets, env)
		else:
			v = self.use(p, env)
			
		self.uses -= 1
		if self.uses == 0:
			p.remove_item(self)

		return v


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
			score=utils.RawScore(s=ss.Scores.Vit,m=2))]