from dataclasses import dataclass

class Action:
	pass

@dataclass
class DoNothing:
	player: object

	def apply(self):
		pass

	@property
	def msg(self):
		return f"{self.player} did absolutely nothing."

@dataclass
class DamageTarget:
	attacker: object
	defender: object
	dmg: int

	def apply(self):
		self.defender.damage(self.dmg)

	@property
	def msg(self):
		return f"{self.attacker.name} deals {self.dmg} damage to {self.defender.name}."


@dataclass
class HealTarget:
	attacker: object
	defender: object
	dmg: int

	def apply(self):
		self.defender.damage(-self.dmg)

	@property
	def msg(self):
		return f"{self.attacker.name} heals {self.dmg} life to {self.defender.name}."

@dataclass
class Miss:
	attacker: object
	defender: object
	ability: str

	def apply(self):
		pass

	@property
	def msg(self):
		return f"{self.attacker.name} missed {self.defender.name} with {self.ability}."