import os
import ast
import requests
import enum
import json
import random
import enum
import ast
import math
import sys
import diskcache as dc
import pathlib
import atexit
from dataclasses import dataclass, fields



CACHE_DIR = pathlib.Path(os.path.join(os.path.split(__file__)[0], "../databases"))
STATE_DIR = pathlib.Path(os.path.join(os.path.split(__file__)[0], "../databases/state"))
PLAYER_CACHE = dc.Cache(CACHE_DIR)
STATE_CACHE = dc.Cache(STATE_DIR)


_MODIFIED = set()

def auto_commit(f):
	def wrapper(ref, *args, **kwds):
		if isinstance(ref, Player):
			_MODIFIED.update({ref})
		return f(ref, *args, **kwds)

	return wrapper

def commit_changed():
	for p in _MODIFIED:
		p.commit()

atexit.register(commit_changed)

if "campaign" not in STATE_CACHE:
	STATE_CACHE['campaign'] = "Null"
#URL = "http://localhost:8911/api/"
#HEADERS = {'Content-type': 'application/json; charset=utf-8'}
#RNG_REQUEST = "https://www.random.org/integers/?num={0}&min=1&max=20&col=1&base=10&format=plain&rnd=new"


def stat_ratio(d1, d2):
	return sum(d1)/(sum(d1) + sum(d2))

def roll_against(s1, p1, s2, p2):
	s1 = [p1.get_skill_amt(s.name) for s in s1]
	s2 = [p2.get_skill_amt(s.name) for s in s2]
	ratio = sum(s1)/(sum(s1) + sum(s2))
	thresh = int(20 * ratio)

	roll = roll_dice()[0]

	return (roll > thresh, thresh, roll)


class Scores(enum.Enum):
	Eva = lambda x: x.eva
	Def = lambda x: x.dfn
	Att = lambda x: x.att
	Acc = lambda x: x.acc

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
class Attributes:
	vigor: int = 1
	strength: int = 1
	endurance: int = 1
	strength: int = 1
	dexterity: int = 1
	intelligence: int = 1
	faith: int = 1
	perception: int = 1
	luck: int = 1

	def increment(self, att):
		att = att.lower()
		f = next(f for f in fields(self) if f.name == att)
		setattr(self, f.name, getattr(self, f.name) + 1)


@dataclass
class Entity:
	name: str
	xp:  int = 0
	hp:  int = 20
	max_hp: int = 20
	status: Statuses = Statuses()
	
	def commit(self):
		pass


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
		base = float(self._acc)

		if self.accup > 0:
			base *= 1.2
		if self.accdown > 0:
			base *= 0.8
		if self.encourage > 0:
			base *= 1.2
		if self.poison > 0:
			base *= 0.7

		return math.ceil(base)
	
	@property
	def att(self):
		base = float(self._att)
		if self.attup > 0:
			base *= 1.2
		if self.attdown > 0:
			base *= 0.8
		if self.encourage > 0:
			base *= 1.1
		if self.poison > 0:
			base *= 0.7

		return math.ceil(base)

	@property
	def eva(self):
		base = float(self._eva)

		if self.evaup > 0:
			base *= 1.2
		if self.evadown > 0:
			base *= 0.8
		if self.encourage > 0:
			base *= 1.1

		return math.ceil(base)

	@property
	def dfn(self):
		base = float(self._dfn)

		if self.defup > 0:
			base *= 1.2
		if self.defdown > 0:
			base *= 0.8
		if self.encourage > 0:
			base *= 1.1

		return math.ceil(base)


	def duel_action(self, actor, party, opponents):
		return actions.DoNothing(player=actor)


	@auto_commit
	def damage(self, v):
		self.hp = min(max(self.hp - v, 0), self.max_hp)


	@property
	def block(self):
		return self.status.block

	@auto_commit
	def stack_block(self, amt=1):
		self.status.block += 1

	@auto_commit
	def use_block(self, amt=1):
		self.status.block = max(0, self.status.block - amt)

	@property
	def attdown(self):
		return self.status.attdown

	@auto_commit
	def stack_attdown(self, amt=1):
		self.status.attdown += 1

	@auto_commit
	def use_attdown(self, amt=1):
		self.status.attdown = max(0, self.status.attdown - amt)
	
	@property
	def attup(self):
		return self.status.attup

	@auto_commit
	def stack_attup(self, amt=1):
		self.status.attup += 1

	@auto_commit
	def use_attup(self, amt=1):
		self.status.attup = max(0, self.status.attup - amt)

	@property
	def defup(self):
		return self.status.defup


	@auto_commit
	def stack_defup(self, amt=1):
		self.status.defup += 1

	@auto_commit
	def use_defup(self, amt=1):
		self.status.defup = max(0, self.status.defup - amt)

	@property
	def defdown(self):
		return self.status.defdown

	@auto_commit
	def stack_defdown(self, amt=1):
		self.status.defdown += 1

	@auto_commit
	def use_defdown(self, amt=1):
		self.status.defdown = max(0, self.status.defdown - amt)

	@property
	def evaup(self):
		return self.status.evaup

	@auto_commit
	def stack_evaup(self, amt=1):
		self.status.evaup += 1

	@auto_commit
	def use_evaup(self, amt=1):
		self.status.evaup = max(0, self.status.evaup - amt)

	@property
	def evadown(self):
		return self.status.evadown

	@auto_commit
	def stack_evadown(self, amt=1):
		self.status.evadown += 1

	@auto_commit
	def use_evadown(self, amt=1):
		self.status.evadown = max(0, self.status.evadown - amt)

	@property
	def accup(self):
		return self.status.accup


	@auto_commit
	def stack_accup(self, amt=1):
		self.status.accup += 1

	@auto_commit
	def use_accup(self, amt=1):
		self.status.accup = max(0, self.status.accup - amt)

	@property
	def accdown(self):
		return self.status.accdown

	@auto_commit
	def stack_accdown(self, amt=1):
		self.status.accdown += 1

	@auto_commit
	def use_accdown(self, amt=1):
		self.status.accdown = max(0, self.status.accdown - amt)


	@property
	def ripstance(self):
		return self.status.ripstance

	@auto_commit
	def stack_ripstance(self, amt=1):
		self.status.ripstance += 1

	@auto_commit
	def use_ripstance(self, amt=1):
		self.status.ripstance = max(0, self.status.ripstance - amt)

	@property
	def soulmass(self):
		return self.status.soulmass

	@auto_commit
	def stack_soulmass(self, amt=1):
		self.status.soulmass += amt

	@auto_commit
	def use_soulmass(self, amt=1):
		self.status.soulmass = max(0, self.status.soulmass - amt)

	@property
	def burn(self):
		return self.status.burn

	@auto_commit
	def stack_burn(self, amt=1):
		self.status.burn += amt

	def use_burn(self, amt=1):
		self.status.burn = max(0, self.status.burn - amt)

	@property
	def poison(self):
		return self.status.poison

	@auto_commit
	def stack_poison(self, amt=1):
		self.status.poison += amt

	@auto_commit
	def use_poison(self, amt=1):
		self.status.poison = max(0, self.status.poison - amt)

	@property
	def bleed(self):
		return self.status.bleed

	@auto_commit
	def stack_bleed(self, amt=1):
		self.status.bleed += amt

	@auto_commit
	def use_bleed(self, amt=1):
		self.status.bleed = max(0, self.status.bleed - amt)

	@property
	def sealing(self):
		return self.status.sealing

	@auto_commit
	def stack_sealing(self, amt=1):
		self.status.sealing += amt

	@auto_commit
	def use_sealing(self, amt=1):
		self.status.sealing = max(0, self.status.sealing - amt)

	@property
	def stun(self):
		return self.status.stun

	@auto_commit
	def stack_stun(self, amt=1):
		self.status.stun += amt

	@auto_commit
	def use_stun(self, amt=1):
		self.status.stun = max(0, self.status.stun - amt)


	@property
	def invis(self):
		return self.status.invis

	@auto_commit
	def stack_invis(self, amt=1):
		self.status.invis += amt

	@auto_commit
	def use_invis(self, amt=1):
		self.status.invis = max(0, self.status.invis - amt)

	@property
	def encourage(self):
		return self.status.encourage

	@auto_commit
	def stack_encourage(self, amt=1):
		self.status.encourage += amt

	@auto_commit
	def use_encourage(self, amt=1):
		self.status.encourage = max(0, self.status.encourage - amt)

	@property
	def charm(self):
		return self.status.charm

	@auto_commit
	def stack_charm(self, amt=1):
		self.status.charm += amt

	@auto_commit
	def use_charm(self, amt=1):
		self.status.charm = max(0, self.status.charm - amt)

	def get_taunt_target(self):

		return self.status.taunt

	@auto_commit
	def taunt_target(self, target):
		self.status.taunt = target.label

	@auto_commit
	def end_taunt(self):
		self.status.taunt = None
	

	def duel_action(self, actor, party, opponents):
		return [actions.DoNothing(player=actor)]

	def find_valid_target(self, op):
		op = list(filter(lambda x: x.invis == 0 and not x.dead, op))
		return random.choices(op)[0]

	def soulmass_count(self):
		return 0

	@property
	def is_player(self):
		return False

	@property
	def is_npc(self):
		return True

	

	@auto_commit
	def revive(self):
		self.hp = self.max_hp

	@auto_commit
	def reset_status(self):
		self.statu = Statuses()

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		if isinstance(other, Player):
			return self.name == other.name

		return False


import ShrimpSouls.classes as classes

@dataclass
class Player(Entity):
	attributes: Attributes = Attributes()
	myclass: classes.ClassSpec = classes.ClassSpec()

	def __hash__(self):
		return hash(self.name)

	def commit(self):
		PLAYER_CACHE[self.name] = self


	@property
	def level(self):
		fs = fields(self.attributes)

		return sum(getattr(self.attributes, f.name) for f in fs) - (len(fs) - 1)

	@auto_commit
	def level_up(self, att):
		req = self.get_xp_req()
		if self.xp >= req:
			self.xp -= req
			self.attributes.increment(att)
			print(f"{self.name} has leveled up {att}!!!")
			self.commit()
		else:
			raise ValueError(f"{self.name} does not have enough xp to level up. (Has {self.xp}, needs {req})")

	def get_xp_req(self):
		return 0
		if self.level < 1:
			return 100
		else:
			return int(100 * (1.2 ** (self.level - 1)))

	@property
	def stat_string(self):
		s = f"""{self.name}: [Level {self.level} {self.myclass.cl_string}] 
			HP: ({self.hp}/{self.max_hp})
			XP: {self.xp},
			Vigor : {self.attributes.vigor},
			Endurance : {self.attributes.endurance},
			Strength : {self.attributes.strength},
			Dexterity : {self.attributes.dexterity},
			Intelligence : {self.attributes.intelligence},
			Faith : {self.attributes.faith},
			Luck : {self.attributes.luck},
			Perception : {self.attributes.perception},
		"""

		return ' '.join(s.split())

	@property
	def _acc(self):
		return self.myclass.score_acc(self)
	
	@property
	def _att(self):
		return self.myclass.score_att(self)

	@property
	def _eva(self):
		return self.myclass.score_eva(self)

	@property
	def _dfn(self):
		return self.myclass.score_dfn(self)

	def duel_action(self, actor, party, opponents):
		return self.myclass.duel_action(actor, party, opponents)

	@property
	def is_player(self):
		return True

	@auto_commit
	def add_shrimp(self, amt):
		self.xp += amt

	def soulmass_count(self):
		return self.myclass.soulmass_count(self)
	

_FETCHED_PLAYERS = {}

def get_player(name, init=False):
	if name in _FETCHED_PLAYERS:
		return _FETCHED_PLAYERS[name]
	else:
		if name not in PLAYER_CACHE and init:
			player = Player(name=name)
			PLAYER_CACHE[name] = player

		else:
			player = PLAYER_CACHE[name]

		_FETCHED_PLAYERS[name] = player
		return player

	
def level_up(name, stat):
	get_player(name, init=True).level_up(stat)

def update_class(name, clname):
	p = get_player(name, init=True)
	p.myclass = classes.Classes[clname.lower().capitalize()].value
	p.commit()
	print(f"{p.name} has updated their class to {p.myclass.cl_string}!!!")


def main(args):
	if args[0] == "stats":
		print(get_player(args[1], init=True).stat_string)
	elif args[0] == "levelup":
		level_up(args[1], args[2])
	elif args[0] == "updateclass":
		update_class(args[1], args[2])
	elif args[0] == "campaigntype":
		print(f"The current campaign is {STATE_CACHE['campaign']}")
	elif args[0] == 'step':
		import ShrimpSouls.campaigns as cps
		cps.Campaigns[STATE_CACHE['campaign']].value.step()
	elif args[0] == 'startcampaign':
		import ShrimpSouls.campaigns as cps
		ctype = cps.Campaigns[args[1].lower().capitalize()]
		STATE_CACHE['campaign'] = ctype.name
		print(ctype.value.start_msg)
	elif args[0] == "join":
		p = get_player(args[1])
		import ShrimpSouls.campaigns as cps
		cps.Campaigns[STATE_CACHE['campaign']].value.join(args[1])

	elif args[0] == "basicclassaction":		
		import ShrimpSouls.campaigns as cps
		c = cps.Campaigns[STATE_CACHE['campaign']].value
		p = get_player(args[1], init=True)
		p.myclass.basic_action(p, c)
		c.commit()

	elif args[0] == "targetclassaction":		
		import ShrimpSouls.campaigns as cps
		c = cps.Campaigns[STATE_CACHE['campaign']].value
		p = get_player(args[1], init=True)
		p.myclass.targeted_action(p, args[2], c)
		c.commit()

	elif args[0] == "foelist":
		import ShrimpSouls.campaigns as cps
		c = cps.Campaigns[STATE_CACHE['campaign']].value.foes()





