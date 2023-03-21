import enum
import ShrimpSouls as ss
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
from dataclasses import dataclass
import persistent

class ArmorSlot(enum.Enum):
	Chest = enum.auto()
	Legs = enum.auto()
	Helmet = enum.auto()
	Gloves = enum.auto()
	Ring = enum.auto()


class WeaponType(enum.Enum):
	Sword = enum.auto()
	Greatsword = enum.auto()
	GreatHammer = enum.auto()



@dataclass
class Armor:
	slot: ArmorSlot
	acc: int = 0
	eva: int = 0
	att: int = 0
	dfn: int = 0
	will: int = 0
	vit: int = 0
	char: int = 0
	fort: int = 0

@dataclass
class Weapon:
	Slash: int = 0
	Strike: int = 0
	Pierce: int = 0
	Fire: int = 0
	Magic: int = 0
	Lightning: int = 0
	Dark: int = 0
	Nature: int = 0
	Holy: int = 0

	"""
	def get_damage(self, t):
		match t:
			yield (actions.DamageType.Slash, self.Slash)
			yield (actions.DamageType.Strike, self.Strike)
			yield (actions.DamageType.Pierce, self.Pierce)
			yield (actions.DamageType.Fire, self.Fire)
			yield (actions.DamageType.Magic, self.Magic)
			yield (actions.DamageType.Lightning, self.Lightning)
			yield (actions.DamageType.Dark, self.Dark)
			yield (actions.DamageType.Nature, self.Nature)
			yield (actions.DamageType.Holy, self.Holy)
	"""


@dataclass
class Item(persistent.Persistent):
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

class EquipItem(persistent.Persistent):
	def __init__(self, item):
		self.__item = item 
		
	def act(self, p, targets, env):
		return []


	def use(self, p, env):
		return []

	def apply(self, p, targets, env):
		return []

import ShrimpSouls.items.armor as armor
import ShrimpSouls.items.weapons as weapons

@dataclass
class Equipment
	body: Armor = armor.ClothArmor
	hands: Armor = armor.ClothGloves
	legs: Armor = armor.ClothLegs
	head: Armor = armor.ClothHelmet

	rhand: Weapon = weapons.BareHand
	lhand: Weapon = weapons.BareHand