import enum
import math
import functools as ftools
from dataclasses import dataclass, field
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

class Tags(enum.Enum):
	Unblockable = enum.auto()
	Unparriable = enum.auto()


@dataclass
class Action:
	attacker: object
	defender: object
	msg: str = ''

	def on_hit(self):
		pass

	def on_miss(self):
		pass

	@property	
	def receivers(self):
		if self.attacker is not None and self.attacker.is_player:
			if self.defender is not None and self.defender.is_player:
				return (self.attacker, self.defender)
			else:
				return tuple()
		elif self.defender is not None and self.defender.is_player:
			return (self.defender,)

		else:
			return tuple()

	@property	
	def receivers_npc(self):
		if self.attacker is not None and self.attacker.is_npc:
			if self.defender is not None and self.defender.is_npc:
				return (self.attacker, self.defender)
			else:
				return tuple()
		elif self.defender is not None and self.defender.is_npc:
			return (self.defender,)

		else:
			return tuple()



@dataclass
class DoNothing:
	player: object

	def apply(self):
		pass

	@property
	def msg(self):
		return f"{self.player.name} did absolutely nothing."


	@property	
	def receivers(self):
		return tuple()

	@property	
	def receivers_npc(self):
		return tuple()




@dataclass
class HealTarget(Action):
	attacker: object
	defender: object
	
	msg: str = ''
	dmg: int = 0

	def apply(self):
		if not self.defender.dead:
			amt = math.ceil(self.attacker.att/20)
			self.msg += f"{self.attacker.name} heals {amt} life to {self.defender.name}."
			self.defender.damage(-amt)	
			
		else:
			self.msg += f"{self.attacker.name} could not heal dead target {self.defender.name}."

			


@dataclass
class ReviveTarget(Action):
	attacker: object
	defender: object
	
	msg: str = ''
	dmg: int = 0

	def apply(self):
		amt = math.ceil(self.attacker.att/40)
		self.defender.damage(-amt)
		f"{self.attacker.name} revives {self.defender.name} for {amt} life. Wokege"



@dataclass
class Error:
	info: str 

	@property
	def msg(self):
		return f"ERROR: {self.info}"

	def apply(self):
		pass

	@property	
	def receivers(self):
		return tuple()

	@property	
	def receivers(self):
		return tuple()

	@property	
	def receivers_npc(self):
		return tuple()



@dataclass
class DamageTarget(Action):
	attacker: object
	defender: object
	score_hit: tuple = utils.score_hit()
	score_dmg: tuple = utils.score_dmg()
	dmgtype: DamageType = DamageType.Slash
	abilityrange: AbilityRange = AbilityRange.Close
	msg: str = ""
	applied: bool = False
	statuses: tuple = tuple()


	def apply(self):
		if self.applied:
			return self.msg
		elif self.attacker is None or self.defender is None:
			pass
		elif self.attacker.dead:
			self.msg = f"{self.attacker.name} cannot attack while dead."
		elif self.defender.dead:
			self.msg = f"{self.defender.name} cannot be attacked while dead."
		elif self.attacker.stun > 0:
			self.msg = f"{self.attacker.name} was stunned and could not act."
		else:
			self.applied = True

			if self.defender.ripstance > 0 and self.abilityrange.can_riposte():
				self.parry_scenario()
			elif self.defender.soulmass > 0 and self.abilityrange.can_soulmass():
				self.soulmass_scenario()
			else:
				self.standard_scenario()				

			if self.attacker.dead:
				self.msg += f"{self.attacker.name} has died."

			if self.defender.dead:
				self.msg += f"{self.defender.name} has died."


		return self.msg

	def standard_scenario(self):
		hits = utils.compute_bool_many(self.attacker, self.defender, *self.score_hit)

		total = 0
		for h in hits:
			if h:
				d = utils.compute_dmg(self.attacker, self.defender, *self.score_dmg)
				dmg = d if self.defender.block == 0 else math.ceil(d * 0.25)
				total += dmg

				
		if total == 0:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."
		else:
			self.on_hit()
			self.__apply_status()
			if self.defender.weak(self.dmgtype):
				total = math.ceil(1.5 * total)
			if self.defender.resist(self.dmgtype):
				total = math.ceil(0.5 * total)

			self.msg += f"{self.attacker.name} attacks {self.defender.name} for {total} damage. "
			self.defender.damage(total)

	def soulmass_scenario(self):
		totals = [
			utils.compute_bool(self.defender, self.attacker, *self.score_hit) 
			for _ in range(self.defender.soulmass_count())]
		dmg = sum(
			utils.compute_dmg(self.defender, self.attacker, *self.score_dmg)
			for t in totals if t)
		self.attacker.damage(dmg)
		self.defender.use_soulmass(amt=1)

		if dmg > 0:
			if self.defender.weak(DamageType.Magic):
				dmg = math.ceil(1.5 * dmg)
			self.msg += f"{self.attacker.name} provokes {self.defender.name}'s Soulmasses and suffers {dmg} damage."


		self.standard_scenario()

	def parry_scenario(self):
		parry = utils.compute_bool(self.defender, self.attacker, *self.score_hit)
		if parry:
			riposte = utils.compute_bool(self.defender, self.attacker, *self.score_hit)
			if riposte:
				d = utils.compute_dmg(self.defender, self.attacker, *self.score_dmg)
				self.attacker.damage(d)
				self.msg += f"{self.defender.name} parries and ripostes {self.attacker.name} for {d} damage."
			else:
				h = utils.compute_bool(self.attacker, self.defender, *self.score_hit)
				if h:
					d = utils.compute_dmg(self.attacker, self.defender, *self.score_dmg)//2
					self.defender.damage(d)
					self.msg += f"{self.defender.name} manages to partially parry {self.attacker.name}'s attack, and suffers {d} damage."
				else:
					self.msg += f"{self.attacker.name} missed {self.defender.name}."
		else:
			self.standard_scenario()

	def __apply_status(self):
		for (s, a) in self.statuses:
			s.stack(self.defender, amt=a)

		if len(self.statuses) > 0:
			self.msg += f"{self.defender.name} was afflicted with {', '.join(s[0].name for s in self.statuses)}. "


	


@dataclass
class EffectAction(Action):
	attacker: object
	defender: object
	score_hit: tuple = utils.score_hit()
	score_dmg: tuple = utils.score_dmg()
	abilityrange: AbilityRange = AbilityRange.Close
	msg: str = ""
	applied: bool = False

	def apply(self):
		if self.applied:
			return self.msg
		elif self.attacker is None or self.defender is None:
			pass
		elif self.attacker.dead:
			self.msg = f"{self.attacker.name} cannot attack while dead."
		elif self.defender.dead:
			self.msg = f"{self.defender.name} cannot be attacked while dead."
		elif self.attacker.stun > 0:
			self.msg = f"{self.attacker.name} was stunned and could not act."
		else:
			if utils.compute_bool(self.attacker, self.defender, *self.score_hit):
				self.on_hit()
			else:
				self.on_miss()

	

