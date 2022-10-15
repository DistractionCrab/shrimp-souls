import enum
import math
from dataclasses import dataclass
import ShrimpSouls.utils as utils
import ShrimpSouls as ss


class DamageType(enum.Enum):
	Slash = enum.auto()
	Strike = enum.auto()
	Pierce = enum.auto()
	Fire = enum.auto()
	Magic = enum.auto()
	Lightning = enum.auto()
	Dark = enum.auto()

	@property
	def physical(self):
		return self in [DamageType.Slash, DamageType.Strike, DamageType.Pierce]

	@property
	def non_physical(self):
		return self in [DamageType.Fire, DamageType.Magic, DamageType.Lightning, DamageType.Dark]

	

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
		return f"{self.player.name} did absolutely nothing."

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
		if self.attacker.dead:
			msg += f"{self.attacker.name} cannot attack while dead."
		elif self.defender.dead:
			msg += f"{self.defender.name} cannot be attacked while dead."
		else:
			if self.defender.ripstance > 0 and self.abilityrange.can_riposte():
				(parry, a1, d1) = self.parry
				(riposte, a2, d2) = self.riposte
				(hit, a3, d3) = self.hit
				if parry and self.riposte:
					dmg = utils.compute_dmg(self.defender, self.attacker)[0]
					self.attacker.damage(dmg)
					msg += f"{self.defender.name} parries and ripostes {self.attacker.name} for {dmg} damage. ({a1} vs {d1} and {a2} vs {d2})"
				elif parry and hit:
					dmg = math.ceil(self.dmg[0]/2)
					self.defender.damage(dmg)
					msg += f"{self.defender.name} manages to partially parry {self.attacker.name}'s attack, and suffers {dmg} damage. ({a1} vs {d1} and {a3} vs {d3})"
				else:
					msg += f"{self.attacker.name} missed {self.defender.name}. ({a3} vs {d3})"
			elif self.defender.soulmass > 0 and self.abilityrange.can_soulmass():
				totals = [
					utils.compute_hit(self.defender, self.attacker) 
					for _ in range(self.defender.soulmass_count())]
				dmg = sum(
					utils.compute_dmg(self.defender, self.attacker)[0]
					for t in totals if t[0])
				self.attacker.damage(dmg)

				msg += f"{self.attacker.name} provokes {self.defender.name}'s Soulmasses and suffers {dmg} damage. "

				if self.hit:
					dmg = self.dmg[0]
					self.defender.damage(dmg)
					msg += f"{self.attacker.name} attacks {self.defender.name} for {dmg} damage. "
				else:
					msg += f"{self.attacker.name} missed {self.defender.name}."
			else:
				(hit, a, d) = self.hit
				if hit:
					if self.defender.block > 0:
						(dmg, a2, d2) = self.dmg
						dmg = math.ceil(dmg*0.75)
						self.defender.damage(dmg)
						self.defender.use_block()
						msg += f"{self.attacker.name} attacks {self.defender.name} for {dmg} damage. ({a} vs {d} and {a2} vs {d2}) "
					else:
						(dmg, a2, d2) = self.dmg
						self.defender.damage(dmg)
						msg += f"{self.attacker.name} attacks {self.defender.name} for {dmg} damage. ({a} vs {d} and {a2} vs {d2}) "
				else:
					msg += f"{self.attacker.name} missed {self.defender.name}. ({a} vs {d}) "

			if self.attacker.dead:
				msg += f"{self.attacker.name} has died."

			if self.defender.dead:
				msg += f"{self.defender.name} has died."


		self.msg = msg
		return self.msg

	def deal_damage(self, attacker, target, amt):
		msg = f'{attacker.name} deals {amt} damage to {target.name}. '
		target.dmg(amt)
		if target.dead:
			msg += f'{attacker.name} has slain {target.name}'

		return msg

	@property
	def dmg(self):
		if self.dmgoverride is None:
			return utils.compute_dmg(self.attacker, self.defender)
		else:
			return (self.dmgoverride, None, None)

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