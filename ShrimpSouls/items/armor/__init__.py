import ShrimpSouls.items as items
from dataclasses import dataclass

@dataclass
class ClothArmor(items.Armor):
	slot: items.ArmorSlot = items.ArmorSlot.Chest

@dataclass
class ClothHelmet(items.Armor):
	slot: items.ArmorSlot = items.ArmorSlot.Helmet

@dataclass
class ClothGloves(items.Armor):
	slot: items.ArmorSlot = items.ArmorSlot.Gloves

@dataclass
class ClothLegs(items.Armor):
	slot: items.ArmorSlot = items.ArmorSlot.Legs