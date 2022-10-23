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


@dataclass
class Action:
	attacker: object
	defender: object
	msg: str = ''



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
class ReviveTarget:
	attacker: object
	defender: object
	dmg: int

	def apply(self):
		self.defender.damage(-self.dmg)

	@property
	def viable(self):
		return not self.defender.dead
			

	@property
	def msg(self):
		return f"{self.attacker.name} revives {self.defender.name} for {self.dmg} life."


_DEFAULT_COMBAT_LOG = {
	"act_type": "BasicAttack",
	"attacker": '',
	"defender": '',
	"hits": [],
	"parry": [False, None, None],
	"riposte": [False, None, None],
	"ripostedmg": [False, None, None],
	'smdmg': 0
}


@dataclass
class DamageTarget:
	attacker: object
	defender: object
	dmgoverride: object = None
	dmgtype: DamageType = DamageType.Slash
	abilityrange: AbilityRange = AbilityRange.Close
	msg: str = ""
	clog: dict = field(default_factory=lambda: dict(_DEFAULT_COMBAT_LOG))
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
			self.clog["attacker"] = self.attacker.name
			self.clog["defender"] = self.defender.name

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
		hits = utils.compute_bool_many(
			self.attacker, 
			self.defender, 
			ss.Scores.Acc,
			ss.Scores.Eva)

		total = 0
		for h in hits:
			if h[0]:
				d = utils.compute_dmg(self.attacker, self.defender)
				dmg = d[0] if self.defender.block == 0 else math.ceil(d[0] * 0.25)
				total += dmg
			else:
				d = (None, None, None)

			self.clog['hits'].append((h, d))
				
		if total == 0:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."
		else:
			self.msg += f"{self.attacker.name} attacks {self.defender.name} for {total} damage. "
			self.defender.damage(total)

	def soulmass_scenario(self):
		totals = [
			utils.compute_hit(self.defender, self.attacker) 
			for _ in range(self.defender.soulmass_count())]
		dmg = sum(
			utils.compute_dmg(self.defender, self.attacker)[0]
			for t in totals if t[0])
		self.attacker.damage(dmg)
		self.defender.use_soulmass(amt=1)
		self.clog['smdmg'] = dmg

		if dmg > 0:
		 	self.msg += f"{self.attacker.name} provokes {self.defender.name}'s Soulmasses and suffers {dmg} damage."


		self.standard_scenario()

	def parry_scenario(self):
		parry = utils.compute_hit(self.defender, self.attacker)
		self.clog['parry'] = parry
		if parry[0]:
			riposte = utils.compute_hit(self.defender, self.attacker)
			self.clog['riposte'] = riposte
			if riposte[0]:
				d = utils.compute_dmg(self.defender, self.attacker)
				self.attacker.damage(d[0])
				self.clog['ripostedmg'] = d
				self.msg += f"{self.defender.name} parries and ripostes {self.attacker.name} for {d[0]} damage."
			else:
				h = utils.compute_hit(self.attacker, self.defender)
				if h[0]:
					d = list(utils.compute_dmg(self.attacker, self.defender))
					d[0] = d[0]//2
					self.defender.damage(d[0])
					self.clog['hits'].append((h, d))
					self.msg += f"{self.defender.name} manages to partially parry {self.attacker.name}'s attack, and suffers {d[0]} damage."
				else:
					self.clog['hits'].append((h, (None, None, None)))
					self.msg += f"{self.attacker.name} missed {self.defender.name}."



