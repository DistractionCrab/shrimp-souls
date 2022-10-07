from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls as ss
import random

@dataclass
class Statuses:
	block: int = 0
	attup: int = 0
	attdown: int = 0
	defup: int = 0
	defdown: int = 0
	evaup: int = 0
	evadown: int = 0
	accup: int = 0
	accdown: int = 0
	burn: int = 0
	poison: int = 0
	stun: int = 0
	invis: int = 0
	encourage: int = 0
	soulmass: int = 0
	ripstance: int = 0
	sealing: int = 0

@dataclass
class BaseNPC:
	npcid: int
	name: str
	xp:  int = 1
	hp:  int = 1
	max_hp: int = 1
	acc: int = 1
	eva: int = 1
	att: int = 1
	dfn: int = 1
	status: Statuses = Statuses()


	@property
	def dead(self):
		return self.hp <= 0

	def tick(self):
		if self.burn > 0:
			self.use_burn()
			self.damage(random.randint(1, 4))
		if self.stun > 0:
			self.use_stun()
		if self.invis > 0:
			self.use_invis()


	def duel_action(self, actor, party, opponents):
		return actions.DoNothing(player=actor)

	def compute_hit(self, a, d):
		check = max(min(d.eva - a.acc + 10, 20), 1)
		roll = ss.roll_dice(1)[0]

		return (roll != 1 and roll > check) or roll == 20


	def compute_dmg(self, a, d):
		m = min(max(d.dfn - a.att + 10, 1), 20)

		return ss.roll_dice(max_r=m)[0]

	def damage(self, v):
		self.hp -= v


	@property
	def block(self):
		return self.status.block

	def stack_block(self, amt=1):
		self.status.block += 1

	def use_block(self, amt=1):
		self.status.block = max(0, self.status.block - amt)

	@property
	def attdown(self):
		return self.status.attdown

	def stack_attdown(self, amt=1):
		self.status.attdown += 1

	def use_attdown(self, amt=1):
		self.status.attdown = max(0, self.status.attdown - amt)
	
	@property
	def attup(self):
		return self.status.attup

	def stack_attup(self, amt=1):
		self.status.attup += 1

	def use_attup(self, amt=1):
		self.status.attup = max(0, self.status.attup - amt)

	@property
	def defup(self):
		return self.status.defup

	def stack_defup(self, amt=1):
		self.status.defup += 1

	def use_defup(self, amt=1):
		self.status.defup = max(0, self.status.defup - amt)

	@property
	def defdown(self):
		return self.status.defdown

	def stack_defdown(self, amt=1):
		self.status.defdown += 1

	def use_defdown(self, amt=1):
		self.status.defdown = max(0, self.status.defdown - amt)

	@property
	def evaup(self):
		return self.status.evaup

	def stack_evaup(self, amt=1):
		self.status.evaup += 1

	def use_evaup(self, amt=1):
		self.status.evaup = max(0, self.status.evaup - amt)

	@property
	def evadown(self):
		return self.status.evadown

	def stack_evadown(self, amt=1):
		self.status.evadown += 1

	def use_evadown(self, amt=1):
		self.status.evadown = max(0, self.status.evadown - amt)

	@property
	def accup(self):
		return self.status.accup

	def stack_accup(self, amt=1):
		self.status.accup += 1

	def use_accup(self, amt=1):
		self.status.accup = max(0, self.status.accup - amt)

	@property
	def accdown(self):
		return self.status.accdown

	def stack_accdown(self, amt=1):
		self.status.accdown += 1

	def use_accdown(self, amt=1):
		self.status.accdown = max(0, self.status.accdown - amt)


	@property
	def ripstance(self):
		return self.status.ripstance

	def stack_ripstance(self, amt=1):
		self.status.ripstance += 1

	def use_ripstance(self, amt=1):
		self.status.ripstance = max(0, self.status.ripstance - amt)

	@property
	def soulmass(self):
		return self.status.soulmass

	def stack_soulmass(self, amt=1):
		self.status.soulmass += 1

	def use_soulmass(self, amt=1):
		self.status.soulmass = max(0, self.status.soulmass - amt)

	@property
	def burn(self):
		return self.status.burn

	def stack_burn(self, amt=1):
		self.status.burn += 1

	def use_burn(self, amt=1):
		self.status.burn = max(0, self.status.burn - amt)

	@property
	def poison(self):
		return self.status.poison

	def stack_poison(self, amt=1):
		self.status.poison += 1

	def use_poison(self, amt=1):
		self.status.poison = max(0, self.status.poison - amt)

	@property
	def sealing(self):
		return self.status.sealing

	def stack_sealing(self, amt=1):
		self.status.sealing += 1

	def use_sealing(self, amt=1):
		self.status.sealing = max(0, self.status.sealing - amt)

	@property
	def stun(self):
		return self.status.stun

	def stack_stun(self, amt=1):
		self.status.stun += 1

	def use_stun(self, amt=1):
		self.status.stun = max(0, self.status.stun - amt)


	@property
	def invis(self):
		return self.status.invis

	def stack_invis(self, amt=1):
		self.status.invis += 1

	def use_invis(self, amt=1):
		self.status.invis = max(0, self.status.invis - amt)

	@property
	def encourage(self):
		return self.status.encourage

	def stack_encourage(self, amt=1):
		self.status.encourage += 1

	def use_encourage(self, amt=1):
		self.status.encourage = max(0, self.status.encourage - amt)

	@property
	def xp(self):
		return 0
	
	@property
	def hp(self):
		return self.health

	@property
	def acc(self):
		return self.myclass.value.score_acc(self)
	
	@property
	def att(self):
		return self.myclass.value.score_att(self)

	@property
	def eva(self):
		return self.myclass.value.score_eva(self)

	@property
	def dfn(self):
		return self.myclass.value.score_def(self)

	def duel_action(self, actor, party, opponents):
		return [actions.DoNothing(player=actor)]

	def find_valid_target(self, op):
		op = list(filter(lambda x: x.invis == 0, op))
		return random.choices(op)[0]

	def __hash__(self):
		return hash((self.name, self.npcid))
	

@dataclass
class Goblin(BaseNPC):
	name: str = "Goblin"
	xp:  int = 1
	hp:  int = 5
	max_hp: int = 5
	acc: int = 3
	eva: int = 5
	att: int = 4
	dfn: int = 2

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)

		if super().compute_hit(actor, target):
			dmg = super().compute_dmg(actor, target)

			return [actions.DamageTarget(attacker=actor, defender=target, dmg=dmg)]
		else:
			return [actions.Miss(attacker=actor, defender=target, ability="a swing of the club.")]


def string_to_npcs(s):
	return eval(s)