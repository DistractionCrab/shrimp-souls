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
import pathlib
import atexit
import persistent
import persistent.mapping
import ShrimpSouls.messages as messages

from dataclasses import dataclass, fields, field




def xp_req(l):
	if l < 1:
		return 100
	else:
		return int(100 * (1.2 ** (l - 1)))

def auto_commit(f):
	def wrapper(ref, *args, **kwds):
		v = f(ref, *args, **kwds)
		ref.commit()
		return v

	return wrapper



class Scores(enum.Enum):
	Eva = lambda x: x.eva
	Def = lambda x: x.dfn
	Att = lambda x: x.att
	Acc = lambda x: x.acc

class Positions(enum.Enum):
	FRONT = enum.auto()
	BACK = enum.auto()

class StatusEnum(enum.Enum):
	block = enum.auto()
	attup = enum.auto()
	attdown = enum.auto()
	defup = enum.auto()
	defdown = enum.auto()
	evaup = enum.auto()
	evadown = enum.auto()
	accup = enum.auto()
	accdown = enum.auto()
	burn = enum.auto()
	poison = enum.auto()
	stun = enum.auto()
	invis = enum.auto()
	encourage = enum.auto()
	soulmass = enum.auto()
	ripstance = enum.auto()
	sealing = enum.auto()
	charm = enum.auto()
	taunt = enum.auto()
	bleed = enum.auto()

	def stack(self, p, amt=1):
		setattr(p.status, self.name, max(0, amt + getattr(p.status, self.name)))

	def use(self, p, amt=1):
		setattr(p.status, self.name, max(0, -amt + getattr(p.status, self.name)))

	def get(self, p):
		return  getattr(p.status, self.name)



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

class AttriEnum(enum.Enum):
	Vigor = "vigor"
	Strength = 'strength'
	Endurance = "endurance"
	Dexterity = "dexterity"
	Intelligence = 'intelligence'
	Faith = 'faith'
	Luck = 'luck'
	Perception = 'perception'


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
class Entity(persistent.Persistent):
	name: str
	status: Statuses = field(default_factory=Statuses)
	acted: bool = False

	
	def commit(self):
		pass

	def weak(self, v):
		return False

	def resist(self, v):
		return False

	def has_tag(self, t):
		return False

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
			self.damage(math.ceil(random.randint(1,10) * (1 + self.max_hp//100)))
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

		return utils.acc_scale(self, base)
	
	@property
	def att(self):
		base = float(self._att)
		return utils.att_scale(self, base)
	@property
	def eva(self):
		base = float(self._eva)
		return utils.eva_scale(self, base)

	@property
	def dfn(self):
		base = float(self._dfn)
		return utils.def_scale(self, base)


	def duel_action(self, env):
		return actions.DoNothing(player=self)


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
		self.status.taunt = target.name

	@auto_commit
	def end_taunt(self):
		self.status.taunt = None
	

	def find_valid_target(self, op):
		op = list(filter(lambda x: x.invis == 0 and not x.dead, op))
		if len(op) > 0:
			return random.choices(op)[0]
		else:
			return None

	def soulmass_count(self):
		return 0

	@property
	def is_player(self):
		return False

	@property
	def is_npc(self):
		return True

	def immune(self, d):
		return False
	

	@auto_commit
	def revive(self):
		self.hp = self.max_hp

	@auto_commit
	def reset_status(self):
		self.status = Statuses()

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		if type(self) is type(other):
			return self.name == other.name

		return False

	


_MODIFIED = set()
def commit_changed():
	for p in _MODIFIED:
		PLAYER_CACHE[p.name] = p



atexit.register(commit_changed)

import ShrimpSouls.classes as classes

@dataclass
class Player(Entity):
	hp: int = 0
	xp: int = 0
	attributes: Attributes = field(default_factory=Attributes)
	myclass: classes.ClassSpec = classes.ClassSpec()


	def __hash__(self):
		return hash(self.name)

	@property
	def json(self):
		return {
				'name': self.name,
				'hp': self.hp,
				'max_hp': self.max_hp,
				'xp': self.xp,
				'xp_req': self.get_xp_req(),
				'class': self.myclass.cl_string,
				'attributes': self.attributes.__dict__,
				'status': self.status.__dict__
			}

	@property
	def level(self):
		fs = fields(self.attributes)

		return sum(getattr(self.attributes, f.name) for f in fs) - (len(fs) - 1)

	@auto_commit
	def level_up(self, att):
		req = self.get_xp_req()
		if self.xp >= req:
			self.xp -= req
			try:
				self.attributes.increment(att)
			except:
				return messages.Error(msg=[f"{att} does not exist to level up???"])
			return messages.Message(msg=[f"{self.name} has leveled up {att}!!!"])
		else:
			return messages.Error([f"{self.name} does not have enough xp to level up. (Has {self.xp}, needs {req})"])

	def get_xp_req(self):
		return xp_req(self.level)

	@property
	def stat_string(self):
		s = f"""{self.name}: [Level {self.level} {self.myclass.cl_string}] 
			HP: ({self.hp}/{self.max_hp})
			XP: ({self.xp}/{self.get_xp_req()}),
			Vigor : {self.attributes.vigor},
			Endurance : {self.attributes.endurance},
			Strength : {self.attributes.strength},
			Dexterity : {self.attributes.dexterity},
			Intelligence : {self.attributes.intelligence},
			Faith : {self.attributes.faith},
			Luck : {self.attributes.luck},
			Perception : {self.attributes.perception}
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

	def duel_action(self, env):
		return self.myclass.duel_action(self, env)

	@property
	def is_player(self):
		return True

	@auto_commit
	def add_shrimp(self, amt):
		self.xp += amt

	def soulmass_count(self):
		return self.myclass.soulmass_count(self)

	@auto_commit
	def act(self, env):
		return self.myclass.basic_action(self, env)

	@auto_commit
	def target(self, target, env):
		return self.myclass.targeted_action(self, target, env)

	@auto_commit
	def allow_actions(self):
		self.acted = False

	@auto_commit
	def did_act(self):
		self.acted = True

	@property
	def max_hp(self):
		return self.myclass.max_hp(self)

	@property
	def position(self):
		return self.myclass.position


	def random_action(self, u, env):
		return self.myclass.random_action(u, env)

	@property
	def is_npc(self):
		return False

	@auto_commit
	def respec(self):
		l = self.level
		self.attributes = Attributes()

		for i in range(1, l):
			self.add_shrimp(xp_req(i))

		self.hp = min(self.hp, self.max_hp)


	def update_class(self, name):
		self.myclass = classes.Classes[name.lower().capitalize()].value
		self.hp = min(self.hp, self.max_hp)
		return messages.Message(
			msg=f"{self.name} has updated their class to {self.myclass.cl_string}!!!",
			users=[self])


class GameManager(persistent.Persistent):
	def __init__(self):
		import ShrimpSouls.campaigns.arena as cps
		self.__campaign = cps.WaitingRoom()
		self.__players = persistent.mapping.PersistentMapping()

	def step(self):
		(n, msg) = self.__campaign.step()
		if n is not self.__campaign:
			self.__campaign = n

		return msg

	def add_player(self, name):
		if name not in self.__players:
			p = Player(name=name)
			self.__players[name] = p
			return p
		else:
			return self.__players[name]

	def temp_add_player(self, p):
		self.__players[p.name] = p

	def join(self, name):		
		return self.__campaign.join(self.add_player(name))

	def is_joined(self, name):
		return self.__campaign.is_joined(name)

	@property
	def party(self):
		return list(self.campaign.players.values())
	
	@property
	def players(self):
		return list(self.__players.values())

	@property
	def joined_players(self):
		return self.__campaign.players

	def get_player(self, name):
		name = name.lower()
		return self.add_player(name)

	def get_npc(self, name):
		return self.__campaign.get_npc(name)

	@property
	def npcs(self):
		return list(self.__campaign.npcs.values())


	def use_ability(self, name, abi, targets):
		return self.__campaign.use_ability(self.get_player(name), abi, targets)

	@property
	def campaign(self):
		return self.__campaign

	def reset_campaign(self):
		import ShrimpSouls.campaigns.arena as cps
		self.__campaign = cps.WaitingRoom()

	def resting(self, p):
		return True
		return self.__campaign.restarea or not self.__campaign.is_joined(p)

	def respec(self, p, cl):
		if isinstance(p, str):
			p = self.get_player(p)

		if self.resting(p):
			p.update_class(cl)
			p.respec()
			return messages.Message(
				msg=[f"{p.name} has respecced! Their level is reset to 1 and their shrimp is refunded."],
				users=[p])
		else:
			return messages.Error(msg=[f"{p.name} cannot respec in a non-resting arena."])
	

import ShrimpSouls.utils as utils


def main(args):
	import ZODB, persistent
	import persistent.mapping
	import transaction


	DB_PATH = os.path.join(os.path.split(__file__)[0], "../../databases/testing.fs")
	db = ZODB.DB(DB_PATH)
	cn = db.open()

	if "clients" not in cn.root():
		cn.root.clients = persistent.mapping.PersistentMapping()
		game = GameManager()
		cn.root.clients[150659682] = game
	else:
		game = cn.root.clients[150659682]



	if args[0] == "stats":
		print(game.get_player(args[1]).stat_string)
	elif args[0] == "levelup":
		print(game.get_player(args[1]).level_up(args[2])[-1])
	elif args[0] == "updateclass":
		print(game.get_player(args[1]).update_class(args[2]).msg)
	elif args[0] == 'step':
		m = game.step()
		print(m.msg[-1])
		#return
		#for i in m.msg:
		#	print(i)
		#print("-"*30)
	elif args[0] == "foelist":
		print(game.campaign.foes())
	elif args[0] == "join":
		print(game.join(args[1]))
	elif args[0] == "action":
		if len(args) == 2:
			print(f"{args[1]} Must supply ability name to perform action. Use !abilities to list yours.")
		else:
			m = game.use_ability(args[1], args[2], args[3:])
			if m.is_err:
				print(m.msg)
			else:
				print(" ".join(s for s in m.msg))
	elif args[0] == "respec":
		p = game.get_player(args[1])
		p.respec()
		print(f"{p.name} has respeced, getting reset to level 1 and getting shrimp refunded.")

	elif args[0] == "clear":
		game.campaign.clear_npcs()
		game.campaign.clear_players()

	elif args[0] == "abilities":
		p = game.get_player(args[1])
		c = p.myclass
		abis = c.ability_list
		print(f"@{args[1]} Abilities for {c.cl_string} are {abis}")
	elif args[0] == "xp_test":
		p = game.get_player("distractioncrab")
		p.add_shrimp(p.get_xp_req())
	elif args[0] == "reset_testing":
		p = game.get_player("distractioncrab")
		p.respec()
		p.xp = 0
	elif args[0] == "print":

		for p in game.players:
			print(p.name)

	transaction.commit()
	cn.close()
