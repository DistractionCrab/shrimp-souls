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
	Nature = enum.auto()
	Holy = enum.auto()

	@property
	def physical(self):
		return self in [
			DamageType.Slash, 
			DamageType.Strike, 
			DamageType.Pierce,
			Damage.Nature,
		]

	@property
	def non_physical(self):
		return self in [
			DamageType.Fire, 
			DamageType.Magic, 
			DamageType.Lightning, 
			DamageType.Dark, 
		]

	def is_weak(self, p):
		return p.weak(self)

	def apply_mult(self, p, dmg):
		if p.weak(self):
			return math.ceil(dmg*1.5)
		elif p.resist(self):
			return math.ceil(dmg*0.5)
		else:
			return dmg

	

class AbilityRange(enum.Enum):
	Touch = enum.auto()
	Close = enum.auto()
	Medium = enum.auto()
	Long = enum.auto()

	def can_riposte(self):
		return self == AbilityRange.Touch or self == AbilityRange.Close

	def can_soulmass(self):
		return self == AbilityRange.Touch or self == AbilityRange.Close or self == AbilityRange.Medium

	@property
	def can_deflect(self):
		return (
			self == AbilityRange.Medium or
			self == AbilityRange.Long
		)

class Tags(enum.Enum):
	Unblockable = enum.auto()
	Unparriable = enum.auto()

@dataclass
class Action:
	attacker: object
	defender: object
	msg: str = ''

	def apply(self):
		pass

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
	score: utils.RawScore = utils.RawScore()
	ignore_undead: bool = False
	
	msg: str = ''
	dmg: int = 0

	def apply(self):
		import ShrimpSouls.npcs as npcs
		if npcs.NPCTags.Undead.tagged(self.defender) and not self.ignore_undead:
			if not self.defender.dead:
				amt = self.score(self.attacker)
				self.msg += f"{self.attacker.name} deals {amt} damage to {self.defender.name} (Undead)."
				self.defender.damage(amt)	
				
			else:
				self.msg += f"{self.attacker.name} could not damage dead target {self.defender.name}."
		else:
			if not self.defender.dead:
				amt = self.score(self.attacker)
				self.msg += f"{self.attacker.name} heals {amt} life to {self.defender.name}."
				self.defender.damage(-amt)	
				
			else:
				self.msg += f"{self.attacker.name} could not heal dead target {self.defender.name}."

			


@dataclass
class ReviveTarget(Action):
	attacker: object
	defender: object
	base: int = 1
	mult: int = 1/8
	
	msg: str = ''
	dmg: int = 0

	def apply(self):
		amt = math.ceil(self.attacker.att*self.mult + self.base)
		self.defender.damage(-amt)
		self.msg += f"{self.attacker.name} revives {self.defender.name} for {amt} life. Wokege"



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
	score_hit: utils.DualScore = utils.ScoreHit()
	score_dmg: utils.DualScore = utils.ScoreDamage()
	dmgtype: DamageType = DamageType.Slash
	abilityrange: AbilityRange = AbilityRange.Close
	msg: str = ""
	applied: bool = False
	statuses: dict = field(default_factory=dict)
	use_weapon: bool = False


	def apply(self):
		if self.applied:
			return self.msg
		elif self.attacker is None or self.defender is None:
			pass
		elif self.attacker.dead:
			self.msg = f"{self.attacker.name} cannot attack while dead."
		elif self.defender.dead:
			self.msg = f"{self.defender.name} cannot be attacked while dead."
		elif self.attacker.status.stun > 0:
			self.msg = f"{self.attacker.name} was stunned and could not act."
		else:
			self.applied = True

			if self.defender.status.lightwall > 0 and self.abilityrange.can_deflect:
				self.msg += f"{self.defender.name}'s attack was deflected by {self.attacker.name}'s Wall of Solid Light."
			elif self.defender.status.ripstance > 0 and self.abilityrange.can_riposte():
				self.parry_scenario()
			elif self.defender.status.soulmass > 0 and self.abilityrange.can_soulmass():
				self.soulmass_scenario()
			else:
				self.standard_scenario()				

			if self.attacker.dead:
				self.msg += f"{self.attacker.name} has died."

			if self.defender.dead:
				self.msg += f"{self.defender.name} has died."


		return self.msg

	def standard_scenario(self):
		hit = self.score_hit(self.attacker, self.defender)
				
		if hit:
			total = 0
			dmg = self.score_dmg(self.attacker, self.defender)
			dmg = self.dmgtype.apply_mult(self.defender, dmg)

			
			total += dmg
			self.__apply_status()
			self.on_hit()

			if self.attacker.status.sealing > 0:
				ss.StatusEnum.stun.stack(self.defender)
			if self.defender.status.briar:
				self.__handle_briars()	

			if self.use_weapon:
				for	(t, d) in self.attacker.equipment.lhand:
					if d > 0:
						dmg = utils.score_num(d, self.defender.dfn)
						dmg = t.apply_mult(self.defender, dmg)
						self.defender.damage(dmg)
						total += dmg
				for	(t, d) in self.attacker.equipment.rhand:
					if d > 0:
						dmg = utils.score_num(d, self.defender.dfn)
						dmg = t.apply_mult(self.defender, dmg)
						self.defender.damage(dmg)
						total += dmg

			self.defender.damage(total)
			self.msg += f"{self.attacker.name} attacks {self.defender.name} for {total} damage. "
		else:
			self.msg += f"{self.attacker.name} missed {self.defender.name}."
			
			
			

	def soulmass_scenario(self):
		totals = [
			utils.compute_bool(self.defender, self.attacker, *utils.score_hit()) 
			for _ in range(self.defender.soulmass_count())]
		dmg = sum(
			utils.compute_dmg(self.defender, self.attacker, *utils.score_dmg())
			for t in totals if t)
		self.attacker.damage(dmg)
		ss.StatusEnum.soulmass.use(self.defender)

		if dmg > 0:
			if self.defender.weak(DamageType.Magic):
				dmg = math.ceil(1.5 * dmg)
			self.msg += f"{self.attacker.name} provokes {self.defender.name}'s Soulmasses and suffers {dmg} damage."


		self.standard_scenario()

	def parry_scenario(self):
		parry = utils.compute_bool(self.defender, self.attacker)
		if parry:
			riposte = utils.compute_bool(self.defender, self.attacker)
			if riposte:
				d = utils.compute_dmg(self.defender, self.attacker)
				self.attacker.damage(d)
				self.msg += f"{self.defender.name} parries and ripostes {self.attacker.name} for {d} damage."
			else:
				h = utils.compute_bool(self.attacker, self.defender)
				if h:
					d = utils.compute_dmg(self.attacker, self.defender)//2
					self.defender.damage(d)
					self.msg += f"{self.defender.name} manages to partially parry {self.attacker.name}'s attack, and suffers {d} damage."
				else:
					self.msg += f"{self.attacker.name} missed {self.defender.name}."
		else:
			self.standard_scenario()

	def on_hit(self):
		pass

	def on_miss(self):
		pass

	def __handle_briars(self):
		if self.dmgtype == AbilityRange.Close or self.dmgtype == AbilityRange.Touch:
			dmg = utils.compute_dmg(
				self.defender,
				self.attacker,
				s1=ss.Scores.Def,
				m1=self.defender.status.briar*0.05 + 0.5)
			self.msg += f"{self.attacker.name} is damaged by {self.defender.name}'s briars for {dmg} damage."
			self.attacker.damage(dmg)

	def __apply_status(self):
		for (s, a) in self.statuses.items():
			s.stack(self.defender, amt=a())

		if len(self.statuses) > 0:
			self.msg += f"{self.defender.name} was afflicted with {', '.join(s.name for s in self.statuses.keys())}. "


	


@dataclass
class EffectAction(Action):
	attacker: object
	defender: object
	score_hit: utils.DualScore = utils.ScoreHit()
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
		elif self.attacker.status.stun > 0:
			self.msg = f"{self.attacker.name} was stunned and could not act."
		else:
			if self.score_hit(self.attacker, self.defender):
				self.on_hit()
			else:
				self.on_miss()

	def on_hit(self):
		pass

	def on_miss(self):
		pass

	

@dataclass
class StatusAction(Action):
	attacker: object
	defender: object
	score_hit: utils.DualScore = utils.ScoreHit()
	abilityrange: AbilityRange = AbilityRange.Close
	statuses: utils.FrozenDict = utils.FrozenDict({})
	msg: str = ""
	applied: bool = False
	ignore_res: bool = False

	def apply(self):
		if self.applied:
			return self.msg
		elif self.attacker is None or self.defender is None:
			pass
		elif self.attacker.dead:
			self.msg = f"{self.attacker.name} cannot attack while dead."
		elif self.defender.dead:
			self.msg = f"{self.defender.name} cannot be attacked while dead."
		elif self.attacker.status.stun > 0:
			self.msg = f"{self.attacker.name} was stunned and could not act."
		else:
			self.applied = True
			for (s, amt) in self.statuses.items():
				
				if self.defender.immune(s):
					self.msg += f"{self.defender.name} is immune to {s.name}."
				else:
					c1 = self.attacker is self.defender
					c2 = self.score_hit(self.attacker, self.defender)
					if self.ignore_res or c1 or c2:
						a = amt()
						s.stack(self.defender, amt=a)
						self.msg += f"{self.attacker.name} afflicted {s.name} on {self.defender.name} for {a} turns. "
					else:
						self.msg += f"{self.attacker.name} failed to afflict {s.name} on {self.defender.name}. "
