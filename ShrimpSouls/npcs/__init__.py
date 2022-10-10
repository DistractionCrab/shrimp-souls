from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls as ss
import ShrimpSouls.utils as utils
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
	charm: int = 0
	taunt: str = None
	bleed: int = 0

@dataclass
class BaseNPC:
	npcid: int
	name: str
	xp:  int = 1
	hp:  int = 1
	max_hp: int = 1
	_acc: int = 1
	_eva: int = 1
	_att: int = 1
	_dfn: int = 1
	status: Statuses = Statuses()


	@property
	def dead(self):
		return self.hp <= 0

	def tick(self):
		if self.burn > 0:
			self.use_burn()
			self.damage(random.randint(1, 4))
		if self.poison > 0:
			self.use_poison()
			self.damage(random.randint(1, 2))
		self.damage(self.bleed)
		if self.bleed >= 10:
			self.damage(random.rand(1,10) * (1 + self.max_health//20))
			self.use_bleed(amt=10)
		else:
			self.use_bleed()

		self.use_stun()
		self.use_invis()
		self.use_attup()
		self.use_attdown()
		self.use_accup()
		self.use_accdown()
		self.use_evadown()
		self.use_evaup()
		self.use_defdown()
		self.use_defup()
		self.use_ripstance()
		self.use_sealing()
		self.use_encourage()
		self.use_charm()


	@property
	def acc(self):
		bonus = 0
		if self.accup > 0:
			bonus += 2
		if self.accdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1
		if self.point > 0:
			acc -= 3
		return self._acc + bonus
	
	@property
	def att(self):
		bonus = 0
		if self.attup > 0:
			bonus += 2
		if self.attdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1
		if self.poison > 0:
			bonus -= 3

		return self._att + bonus

	@property
	def eva(self):
		bonus = 0
		if self.evaup > 0:
			bonus += 2
		if self.evadown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1

		return self._eva + bonus

	@property
	def dfn(self):
		bonus = 0

		if self.defup > 0:
			bonus += 2
		if self.defdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1

		return self._dfn + bonus

	def is_named(self, name):
		if "[" in name:
			(n, v) = name.split("[")

			return self.name == n and self.npcid == int(v[:-1])
		else:
			return False

	@property
	def label(self):
		return f"{self.name}[{self.npcid}]"

	def duel_action(self, actor, party, opponents):
		return actions.DoNothing(player=actor)

	def compute_hit(self, a, d):
		return utils.compute_hit(a,d)


	def compute_dmg(self, a, d):
		return utils.compute_dmg(a, d)

	def damage(self, v):
		self.hp = max(self.hp - v, 0)


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
	def bleed(self):
		return self.status.bleed

	def stack_bleed(self, amt=1):
		self.status.bleed += 1

	def use_bleed(self, amt=1):
		self.status.bleed = max(0, self.status.bleed - amt)

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
	def charm(self):
		return self.status.charm

	def stack_charm(self, amt=1):
		self.status.charm += 1

	def use_charm(self, amt=1):
		self.status.charm = max(0, self.status.charm - amt)

	def get_taunt_target(self):

		return self.status.taunt

	def taunt_target(self, target):
		self.status.taunt = target.label

	def end_taunt(self):
		self.status.taunt = None

	@property
	def xp(self):
		return 0
	
	@property
	def hp(self):
		return self.health

	@property
	def acc(self):
		return self._acc
	
	@property
	def att(self):
		return self._att

	@property
	def eva(self):
		return self._eva

	@property
	def dfn(self):
		return self._dfn

	def duel_action(self, actor, party, opponents):
		return [actions.DoNothing(player=actor)]

	def find_valid_target(self, op):
		op = list(filter(lambda x: x.invis == 0, op))
		return random.choices(op)[0]

	def soulmass_count(self):
		return 0

	@property
	def is_player(self):
		return False

	@property
	def is_npc(self):
		return True

	def __hash__(self):
		return hash((self.name, self.npcid))

	

@dataclass
class Goblin(BaseNPC):
	name: str = "Goblin"
	xp:  int = 1
	hp:  int = 10
	max_hp: int = 10
	_acc: int = 8
	_eva: int = 9
	_att: int = 4
	_dfn: int = 4

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]


@dataclass
class Wolf(BaseNPC):
	name: str = "Wolf"
	xp:  int = 3
	hp:  int = 25
	max_hp: int = 25
	_acc: int = 12
	_eva: int = 14
	_att: int = 9
	_dfn: int = 7

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]


def string_to_npcs(s):
	return eval(s)