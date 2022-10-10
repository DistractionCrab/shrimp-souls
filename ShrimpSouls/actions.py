import enum
import math
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls as ss


class DamageType(enum.Enum):
	Slash = enum.auto()
	Fire = enum.auto()
	Magic = enum.auto()

class AbilityRange(enum.Enum):
	Touch = enum.auto()
	Close = enum.auto()
	Medium = enum.auto()
	Long = enum.auto()

	def can_riposte(self):
		return self == AbilityRange.Touch or self == AbilityRange.Close

	def can_soulmass(self):
		return self == AbilityRange.Touch or self == AbilityRange.Close or self == AbilityRange.Medium


class Action:
	pass

@dataclass
class DoNothing:
	player: object

	def apply(self):
		pass

	@property
	def viable(self):
		return True

	@property
	def msg(self):
		return f"{self.player.label} did absolutely nothing."

@dataclass
class DamageTarget:
	attacker: object
	defender: object
	dmgoverride: object = None
	dmgtype: DamageType = DamageType.Slash
	abilityrange: AbilityRange = AbilityRange.Close
	msg: object = None

	def apply(self):
		if self.msg is not None:
			return
		msg = ''
		#if self.attacker.dead:
		if False:
			msg += f"{self.attacker.label} cannot attack while dead."
		#elif self.defender.dead:
		elif False:
			msg += f"{self.defender.label} cannot be attacked while dead."
		else:
			if self.defender.ripstance > 0 and self.abilityrange.can_riposte():
				if self.parry and self.riposte:
					dmg = utils.compute_dmg(self.defender, self.attacker)
					self.attacker.damage(dmg)
					msg += f"{self.defender.label} parries and ripostes {self.attacker.label} for {dmg} damage."
				elif not self.parry and self.hit:
					dmg = math.ceil(self.dmg/2)
					self.defender.damage(dmg)
					msg += f"{self.defender.label} manages to partially parry {self.attacker.label}'s attack, and suffers {dmg} damage."
				else:
					msg += f"{self.attacker.label} missed {self.defender.label}."
			elif self.defender.soulmass > 0 and self.abilityrange.can_soulmass():
				totals = [
					utils.compute_hit(self.defender, self.attacker) 
					for _ in range(self.defender.soulmass_count())]
				dmg = sum(
					utils.compute_dmg(self.defender, self.attacker)
					for t in totals if t)
				self.attacker.damage(dmg)

				msg += f"{self.attacker.label} provokes {self.defender.label}'s Soulmasses and suffers {dmg} damage. "

				if self.hit:
					dmg = self.dmg
					self.defender.damage(dmg)
					msg += f"{self.attacker.label} attacks {self.defender.label} for {dmg} damage. "
				else:
					msg += f"{self.attacker.label} missed {self.defender.label}."
			else:
				if self.hit:
					if self.defender.block > 0:
						dmg = math.ceil(self.dmg*0.75)
						self.defender.damage(dmg)
						self.defender.use_block()
						msg += f"{self.attacker.label} attacks {self.defender.label} for {dmg} damage. "
					else:
						dmg = self.dmg
						self.defender.damage(dmg)
						msg += f"{self.attacker.label} attacks {self.defender.label} for {dmg} damage. "
				else:
					msg += f"{self.attacker.label} missed {self.defender.label}."

		self.msg = msg
		return self.msg

	@property
	def dmg(self):
		if self.dmgoverride is None:
			return utils.compute_dmg(self.attacker, self.defender)
		else:
			return self.dmgoverride

	@property
	def parry(self):
		return utils.compute_hit(self.defender, self.attacker)

	@property
	def hit(self):
		return utils.compute_hit(self.attacker, self.defender)
	
	@property
	def riposte(self):
		return utils.compute_hit(self.defender, self.attacker)
	
	
	

	@property
	def viable(self):
		return not self.attacker.dead and not self.defender.dead



@dataclass
class HealTarget:
	attacker: object
	defender: object
	dmg: int

	def apply(self):
		if not self.defender.dead:
			self.defender.damage(-self.dmg)

	@property
	def viable(self):
		return not self.defender.dead
			

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
	def viable(self):
		return True

	@property
	def msg(self):
		return f"{self.attacker.name} missed {self.defender.name} with {self.ability}."

@dataclass
class ApplyStatus:
	attacker: object
	defender: object
	status: ss.Statuses
	scoreDef: ss.Scores
	scoreAtt: ss.Scores
	amt: int = 1


	def apply(self):
		if not self.attacker.dead and not self.defender.dead:
			self.defender.stack_status(self.status, amt=self.amt)

	@property
	def viable(self):
		return not self.attacker.dead and not self.defender.dead

	@property
	def msg(self):
		return f"{self.attacker.name} applies {self.status.name} to {self.defender.name}."