import os
import ast
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
import persistent.mapping as mapping
import persistent.list as plist
import ShrimpSouls.messages as messages

from dataclasses import dataclass, fields, field

def xp_req(l):
	if l < 1:
		return 100
	else:
		return int(100 * (1.2 ** (l - 1)))


class Scores(enum.Enum):
	Eva = lambda x: x.eva
	Def = lambda x: x.dfn
	Att = lambda x: x.att
	Acc = lambda x: x.acc
	Will = lambda x: x.will
	Fort = lambda x: x.fort
	Char = lambda x: x.char
	Vit = lambda x: x.vit



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
	lightwall = enum.auto()
	briar = enum.auto()

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
	lightwall: int = 0
	briar: int = 0

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

	@property
	def json(self):
		return dict(self.__dict__)


@dataclass
class Entity(persistent.Persistent):
	name: str
	status: Statuses = field(default_factory=Statuses)
	inventory: list = field(default_factory=list)
	acted: bool = False

	
	def add_item(self, i):
		self.inventory.append(i)

	def remove_item(self, i):
		try:
			self.inventory.remove(i)
		except:
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
		if self.status.burn > 0:			
			amt = math.ceil(self.att/10) * math.ceil(self.status.burn/10)
			StatusEnum.burn.use(self)
			self.damage(amt)
			yield f"{self.name} suffered {amt} damage from burns."
		if self.status.poison > 0:
			amt = math.ceil(self.dfn/10) * math.ceil(self.status.poison/10)
			StatusEnum.poison.use(self)
			self.damage(amt)
			yield f"{self.name} suffered {amt} damage from poison."
			
		self.damage(self.status.bleed)
		if self.status.bleed >= 10:
			self.damage(math.ceil(random.randint(1,10) * (1 + self.max_hp//100)))
			StatusEnum.bleed.use(self, amt=10)
		else:
			StatusEnum.bleed.use(self)

		StatusEnum.stun.use(self)
		StatusEnum.invis.use(self)
		StatusEnum.attup.use(self)
		StatusEnum.attdown.use(self)
		StatusEnum.accup.use(self)
		StatusEnum.accdown.use(self)
		StatusEnum.evadown.use(self)
		StatusEnum.evaup.use(self)
		StatusEnum.defdown.use(self)
		StatusEnum.defup.use(self)
		StatusEnum.ripstance.use(self)
		StatusEnum.sealing.use(self)
		StatusEnum.encourage.use(self)
		StatusEnum.charm.use(self)
		StatusEnum.briar.use(self)


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

	@property
	def will(self):
		base = float(self._will)
		return utils.will_scale(self, base)

	@property
	def vit(self):
		base = float(self._vit)
		return utils.vit_scale(self, base)

	@property
	def char(self):
		base = float(self._char)
		return utils.char_scale(self, base)

	@property
	def fort(self):
		base = float(self._fort)
		return utils.fort_scale(self, base)


	def duel_action(self, env):
		return actions.DoNothing(player=self)

	def damage(self, v):
		self.hp = min(max(self.hp - v, 0), self.max_hp)


	def get_taunt_target(self):

		return self.status.taunt

	
	def taunt_target(self, target):
		self.status.taunt = target.name

	
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
	
	def revive(self):
		self.hp = self.max_hp

	
	def reset_status(self):
		self.status = Statuses()

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, other):
		if type(self) is type(other):
			return self.name == other.name

		return False


import ShrimpSouls.classes as classes

@dataclass
class Player(Entity):
	hp: int = 0
	xp: int = 0
	attributes: Attributes = field(default_factory=Attributes)
	myclass: classes.ClassSpec = classes.ClassSpec()

	def __post_init__(self):
		self.hp = self.max_hp

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
				'status': self.status.__dict__,
				'scores': {
					"att": self.att,
					"dfn": self.dfn,
					"eva": self.eva,
					"acc": self.acc,
					"will": self.will,
					"fort": self.fort,
					"char": self.char,
					"vit": self.vit,
				},
				"inventory": [i.display for i in self.inventory]
			}

	@property
	def level(self):
		fs = fields(self.attributes)

		return sum(getattr(self.attributes, f.name) for f in fs) - (len(fs) - 1)

	def level_up(self, att):
		req = self.get_xp_req()
		if self.xp >= req:
			self.xp -= req
			try:
				self.attributes.increment(att)
				yield messages.CharInfo(info=self)
				yield messages.Message(
					msg=[f"{self.name} has leveled up {att}!!!"],
					recv=(self.name,))
				
			except:
				yield messages.Message(
					msg=[f"{att} does not exist to level up???"],
					recv=(self.name,))
			
		else:
			yield messages.Message(
				msg=[f"{self.name} does not have enough xp to level up. (Has {self.xp}, needs {req})"],
				recv=(self.name,))

	def level_up_many(self, atts):
		totals = {a: 0 for a in atts}
		for (att, amt) in atts.items():
			for _ in range(amt):
				try:
					if self.xp >= self.get_xp_req():
						self.xp -= self.get_xp_req()
						self.attributes.increment(att)
						totals[att] += 1			
					else:
						yield messages.Message(
							msg=[f"{self.name} does not have enough xp to level up further. (Has {self.xp}, needs {req})"],
							recv=(self.name,))
						break 
				except:
					yield messages.Message(
						msg=[f"No such attribute: {att}"],
						recv=(self.name,))
					break 

		yield messages.CharInfo(info=self)
		for att, amt in totals.items():
			if amt > 0:
				yield messages.Message(
					msg=[f"{self.name} has leveled up {att} {amt} times!!!"],
					recv=(self.name,))
		

			

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

	@property
	def _will(self):
		return self.myclass.score_will(self)

	@property
	def _fort(self):
		return self.myclass.score_fort(self)

	@property
	def _vit(self):
		return self.myclass.score_vit(self)

	@property
	def _char(self):
		return self.myclass.score_char(self)

	@property
	def is_player(self):
		return True

	
	def add_shrimp(self, amt):
		self.xp += amt

	def soulmass_count(self):
		return self.myclass.soulmass_count(self)

	
	def act(self, env):
		return self.myclass.basic_action(self, env)

	
	def target(self, target, env):
		return self.myclass.targeted_action(self, target, env)

	
	def allow_actions(self):
		self.acted = False

	
	def did_act(self):
		self.acted = True

	@property
	def max_hp(self):
		return self.myclass.max_hp(self)



	def random_action(self, env):
		return self.myclass.random_action(self, env)

	def use_ability(self, abi, targets, env):
		return self.myclass.use_ability(self, abi, targets, env)

	@property
	def is_npc(self):
		return False

	
	def respec(self):
		l = self.level
		self.attributes = Attributes()

		for i in range(1, l):
			self.add_shrimp(xp_req(i))

		self.hp = min(self.hp, self.max_hp)


	def update_class(self, name):
		self.myclass = classes.Classes[name.lower().capitalize()].value
		self.hp = min(self.hp, self.max_hp)
		yield messages.Response(
			msg=[f"{self.name} has updated their class to {self.myclass.cl_string}!!!"],
			recv=[self.name])

	

class GameManager(persistent.Persistent):
	def __init__(self):
		import ShrimpSouls.campaigns.arena as arena
		self.__root = arena.Arena()
		self.__players = persistent.mapping.PersistentMapping()

	def step(self):
		yield from self.__root.step()

	@property
	def players(self):
		return self.__root.players
	

	def add_player(self, name):
		if name not in self.__players:
			p = Player(name=name)
			self.__players[name] = p
			return p
		else:
			return self.__players[name]

	def get_player(self, name):
		if isinstance(name, str):
			if name in self.__players:
				return self.__players[name]
			else:
				return self.add_player(name)
		else:
			return name
		

	def connect(self, p):
		p = self.get_player(p)

		yield messages.CharInfo(info=p)

		if p in self.__root:
			
			yield messages.Message(
				msg=["Connected to Game Server."],
				campinfo=self.__root.campinfo(),
				recv=(p.name,))
		else:
			yield messages.Connected(recv=(p.name,))
			

	def join(self, p):	
		p = self.get_player(p)

		if p in self.__root:
			yield messages.Message(
				msg=["You have already joined the campaign."],
				recv=(p.name,))
		else:
			yield from self.__root.add_player(p)


	def action(self, src, msg):
		if isinstance(src, str):
			src = self.__players[src]

		yield from self.__root.action(src, msg)


	def use_ability(self, name, abi, targets):
		yield from self.__root.use_ability(self.get_player(name), abi, targets)

	def use_item(self, name, index, targets):
		yield from self.__root.use_item(self.get_player(name), index, targets)


	def respec(self, p, cl):
		if isinstance(p, str):
			p = self.get_player(p)

		if self.__root.resting(p) or True:			
			p.respec()
			yield messages.Response(
				msg=[f"{p.name} has respecced! Their level is reset to 1 and their shrimp is refunded."],
				recv=[p.name])
			yield from p.update_class(cl)
			yield messages.CharInfo(info=p)
		else:
			yield messages.Response(
				msg=[f"{p.name} cannot respec in a non-resting arena."],
				recv=[p.name])
	

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
