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
import sqlite3 as sql
from datetime import date



STATS_FILE = os.path.join(os.path.split(__file__)[0], "../stats.db")
CAMPAIGN_FILE = os.path.join(os.path.split(__file__)[0], "../campaign.db")
URL = "http://localhost:8911/api/"
HEADERS = {'Content-type': 'application/json; charset=utf-8'}
RNG_REQUEST = "https://www.random.org/integers/?num={0}&min=1&max=20&col=1&base=10&format=plain&rnd=new"

def get_stats_database():
	return sql.connect(STATS_FILE)


def init_stats_database():
	conn = get_stats_database()
	conn.execute("""
		create table if not exists players (
			username      text primary key,
			class         text default "Milquetoast" not null,
			currency      int default 0 not null check (currency >= 0),
			Vigor         int default 1 not null check (Vigor >= 1),
			Strength      int default 1 not null check (Endurance >= 1),
			Endurance     int default 1 not null check (Strength >= 1),
			Dexterity     int default 1 not null check (Dexterity >= 1),
			Intelligence  int default 1 not null check (Intelligence >= 1),
			Faith         int default 1 not null check (Faith >= 1),
			Perception    int default 1 not null check (Perception >= 1),
			Luck          int default 1 not null check (Luck >= 1))
	""")
	conn.execute("""
		create table if not exists status (
			username      text primary key,
			health        int default 20 not null check (health >= 0),
			stamina       int default 20 not null check (stamina >= 0),
			block         int default 0 not null check (block >= 0),
			attdown        int default 0 not null check (attdown >= 0),
			attup        int default 0 not null check (attup >= 0),
			evadown        int default 0 not null check (accdown >= 0),
			evaup        int default 0 not null check (evaup >= 0),
			accdown        int default 0 not null check (accdown >= 0),
			accup        int default 0 not null check (accup >= 0),
			defdown     int default 0 not null check (defdown >= 0),
			defup    int default 0 not null check (defup >= 0),
			ripstance     int default 0 not null check (ripstance >= 0),
			soulmass      int default 0 not null check (soulmass >= 0),
			burn          int default 0 not null check (burn >= 0),
			poison          int default 0 not null check (poison >= 0),			
			sealing       int default 0 not null check (sealing >= 0),
			stun          int default 0 not null check (stun >= 0),
			invis    int default 0 not null check (invis >= 0),
			encourage     int default 0 not null check (encourage >= 0),
			charm         int default 0 not null check (charm >= 0),
			bleed         int default 0 not null check (bleed >= 0),
			taunt         text)
	""")
	conn.commit()

def get_game_database():
	return sql.connect(CAMPAIGN_FILE)


def init_game_database():
	conn = get_game_database()
	conn.execute("""
		create table if not exists combatlog (
			step      integer default 0 primary key autoincrement)
	""")
	conn.execute("""
		create table if not exists campaigninfo (
			step      integer default 0 primary key autoincrement,
			type      text default "Nothing" not null)
	""")
	conn.execute("""
		create table if not exists players (
			username text primary key not null)
	""")
	conn.execute("""
		create table if not exists encounterdata (
			encounterid int default 0 primary key,
			npcs        text default "{}" not null,
			statedata   text default "None" not null,
			finished    boolean default FALSE not null)
	""")
	conn.execute("""
		INSERT INTO campaigninfo (type)
		VALUES ("Nothing")
	""")
	conn.commit()

def get_active_users():
	d = json.loads(requests.get(f"http://localhost:8911/api/chat/users").text)

	return set([a["Username"] for a in d])
	#return [u for u in temp if u.get_shrimp() > 0 or u.level > 1]

def get_xp_req(lvl):
	if lvl < 1:
		return 100
	else:
		return int(100 * (1.2 ** (lvl - 1)))

def stat_ratio(d1, d2):
	return sum(d1)/(sum(d1) + sum(d2))

def roll_against(s1, p1, s2, p2):
	s1 = [p1.get_skill_amt(s.name) for s in s1]
	s2 = [p2.get_skill_amt(s.name) for s in s2]
	ratio = sum(s1)/(sum(s1) + sum(s2))
	thresh = int(20 * ratio)

	roll = roll_dice()[0]

	return (roll > thresh, thresh, roll)



class Stats(enum.Enum):
	Vigor = "vigor"
	Endurance = "endurance"
	Strength = "strength"
	Dexterity = "dexterity"
	Intelligence = "intelligence"
	Faith = "faith"
	Perception = "perception"
	Luck = "luck"

class Statuses(enum.Enum):
	Block = "block"
	Attup = "attup"
	Attdown = "attdown"
	Defup = "defup"
	Defdown = "defdown"
	Accup = "accup"
	Accdown = "accdown"
	Evaup = "evaup"
	Evadown = "evadown"
	Ripstance = "ripstance"
	Soulmass = "soulmass"
	Burn = "burn"
	Poison = "poison"
	Sealing = "sealing"
	Stun = "stun"
	Invis = "invis"
	Encourage = "encourage"
	Charm = "charm"
	Bleed = "bleed"
	Taunt = "taunt"


class Scores(enum.Enum):
	Eva = lambda x: x.eva
	Def = lambda x: x.dfn
	Att = lambda x: x.att
	Acc = lambda x: x.acc


class User:
	def __init__(self, name):
		self.__conn = get_stats_database()
		self.__name = name.lower()

		check = self.__conn.execute(f"""
			select username from players where username="{self.__name}"
		""").fetchall()

		if len(check) == 0:
			self.__conn.execute(f"""
				INSERT INTO players
				(username) VALUES ("{name}")
			""")

		check = self.__conn.execute(f"""
			select username from status where username="{self.__name}"
		""").fetchall()
		if len(check) == 0:
			self.__conn.execute(f"""
				INSERT INTO status
				(username) VALUES ("{name}")
			""")
			self.__conn.commit()

	def __del__(self):
		self.__conn.commit()

	@property
	def name(self):
		return self.__name

	def get_skill_amt(self, name):
		return self.__conn.execute(f"""
			select username, {Stats[name.lower().capitalize()].value} from players where username="{self.__name}"
		""").fetchone()[1]

	def level_up(self, stat):
		req = get_xp_req(self.level)
		if self.get_shrimp() >= req:
			self.__conn.execute(f"""
					UPDATE players
					SET {Stats[stat.lower().capitalize()].value}={Stats[stat.lower().capitalize()].value}+1
					WHERE username="{self.__name}"
				""")
			self.__conn.commit()
			self.add_shrimp(-req)
			print(f"{self.name} has leveled up {stat.lower().capitalize()}!")
		else:
			raise ValueError(f"{self.__name} does not have enough shrimp to level up (needs {req}, current = {self.get_shrimp()})")

		

	def get_stat_vec(self):
		return tuple(self.__conn.execute(f"""
				SELECT username, Vigor, Endurance, Strength, Dexterity, Intelligence, Faith, Perception, Luck
				FROM players
				WHERE username="{self.__name}"
			""").fetchone()[1:])

	@property
	def level(self):
		return sum(self.get_stat_vec()) - 7

	@property
	def vigor(self):
		return self.get_skill_amt("Vigor")
	

	@property
	def strength(self):
		return self.get_skill_amt("Strength")

	@property
	def dexterity(self):
		return self.get_skill_amt("Dexterity")

	@property
	def intelligence(self):
		return self.get_skill_amt("Intelligence")

	@property
	def faith(self):
		return self.get_skill_amt("Faith")

	@property
	def perception(self):
		return self.get_skill_amt("Perception")


	@property
	def luck(self):
		return self.get_skill_amt("Luck")

	@property
	def myclass(self):
		return Classes[self.__conn.execute(f"""
			select username, class from players where username="{self.__name}"
		""").fetchone()[1]]

	def updateclass(self, c):
		self.__conn.execute(f"""
			UPDATE players SET class="{Classes[c.lower().capitalize()].name}" WHERE username="{self.__name}"
		""")

		self.__conn.commit()

		print(f"{self.name} has updated their class to {Classes[c.lower().capitalize()].name}")


	def get_shrimp(self):
		return self.__conn.execute(f"""
			select username, currency from players where username="{self.__name}"
		""").fetchone()[1]

	def add_shrimp(self, amt):
		c = self.get_shrimp()

		if c + amt < 0:
			amt = 0
		else:
			amt = c + amt

		self.__conn.execute(f"""
				UPDATE players
				SET currency={amt}
				WHERE username="{self.__name}"
			""")

		self.__conn.commit()
		return amt

	def stat_string(self):
		s_vec = self.get_stat_vec()
		s = "{name} (Level {level} {cl}): [HP: {hp}, XP: {xp}], Vigor : {vig}, Endurance : {end}, Strength : {st}, Dexterity : {dex}, Intelligence : {int}, Faith : {fth}, Perception : {perc}, Luck : {luck}"
		return s.format(			
			name=self.__name,
			cl=self.myclass.name,
			level=self.level,
			hp=self.health,
			xp=self.get_shrimp(),
			vig=s_vec[0],
			end=s_vec[1],
			st=s_vec[2],
			dex=s_vec[3],
			int=s_vec[4],
			fth=s_vec[5],
			perc=s_vec[6],
			luck=s_vec[7],
		)


	def bonk(self):
		requests.post(
			f"http://localhost:8911/api/commands/5c7e8c45-1fe8-415a-825f-cace3784773a",
			headers=HEADERS,
			data=repr([self.__name]))

	def __get_status(self, val):
		return self.__conn.execute(f"""
			select username, {val} from status where username="{self.__name}"
		""").fetchone()[1]

	def reset_status(self):
		self.__conn.execute(f"""
			DELETE FROM status
			WHERE username="{self.__name}"
		""")
		self.__conn.execute(f"""
				INSERT INTO status
				(username) VALUES ("{self.__name}")
			""")
		self.__conn.commit()

	def revive(self):
		self.__decrement_stat("health", dec=self.health - self.max_health)


	def __decrement_stat(self, value, dec=1):
		v = self.__get_status(value)
		if v - dec >= 0:
			v = v - dec
		else:
			v = 0
		self.__conn.execute(f"""
			UPDATE status
			SET {value}={v}
			WHERE username="{self.__name}"
		""")
		self.__conn.commit()

	@property
	def dead(self):
		return self.health == 0
	

	@property
	def health(self):
		return int(self.__get_status("health"))
	
	@property
	def max_health(self):
		return 20 + 2*(self.vigor - 1)
	

	def damage(self, d):
		if self.health - d >= self.max_health:
			d = self.health - self.max_health
		self.__decrement_stat("health", d)


	def get_status(self, stat):
		return self.__get_status(state.value)

	def stack_status(self, stat, amt=1):
		self.__decrement_stat(stat.value, amt)

	def use_status(self, stat, amt=1):
		self.__decrement_stat(stat.value, amt)

	@property
	def block(self):
		return self.__get_status("block")

	def stack_block(self, amt=1):
		self.__decrement_stat("block", -amt)

	def use_block(self, amt=1):
		self.__decrement_stat("block", amt)

	@property
	def accup(self):
		return self.__get_status("accup")

	def stack_accup(self, amt=1):
		self.__decrement_stat("accup", -amt)

	def use_accup(self, amt=1):
		self.__decrement_stat("accup", amt)

	@property
	def accdown(self):
		return self.__get_status("accdown")

	def stack_accdown(self, amt=1):
		self.__decrement_stat("accdown", -amt)

	def use_accdown(self, amt=1):
		self.__decrement_stat("accdown", amt)


	@property
	def attup(self):
		return self.__get_status("attup")

	def stack_attup(self, amt=1):
		self.__decrement_stat("attup", -amt)

	def use_attup(self, amt=1):
		self.__decrement_stat("attup", amt)

	@property
	def attdown(self):
		return self.__get_status("accdown")

	def stack_attdown(self, amt=1):
		self.__decrement_stat("attdown", -amt)

	def use_attdown(self, amt=1):
		self.__decrement_stat("attdown", amt)

	@property
	def evaup(self):
		return self.__get_status("evaup")

	def stack_evaup(self, amt=1):
		self.__decrement_stat("evaup", -amt)

	def use_evaup(self, amt=1):
		self.__decrement_stat("evaup", amt)

	@property
	def evadown(self):
		return self.__get_status("evadown")

	def stack_evadown(self, amt=1):
		self.__decrement_stat("evadown", -amt)

	def use_evadown(self, amt=1):
		self.__decrement_stat("evadown", amt)

	@property
	def defup(self):
		return self.__get_status("defup")

	def stack_defup(self, amt=1):
		self.__decrement_stat("defup", -amt)

	def use_defup(self, amt=1):
		self.__decrement_stat("defup", amt)

	@property
	def defdown(self):
		return self.__get_status("defdown")

	def stack_defdown(self, amt=1):
		self.__decrement_stat("defdown", -amt)

	def use_defdown(self, amt=1):
		self.__decrement_stat("defdown", amt)


	@property
	def ripstance(self):
		return self.__get_status("ripstance")

	def stack_ripstance(self, amt=1):
		self.__decrement_stat("ripstance", -amt)

	def use_ripstance(self, amt=1):
		self.__decrement_stat("ripstance", amt)


	@property
	def soulmass(self):
		return self.__get_status("soulmass")

	def stack_soulmass(self, amt=1):
		self.__decrement_stat("soulmass", -amt)

	def use_soulmass(self, amt=1):
		self.__decrement_stat("soulmass", amt)

	@property
	def burn(self):
		return self.__get_status("burn")

	def stack_burn(self, amt=1):
		self.__decrement_stat("burn", -amt)

	def use_burn(self, amt=1):
		self.__decrement_stat("burn", amt)

	@property
	def bleed(self):
		return self.__get_status("bleed")

	def stack_bleed(self, amt=1):
		self.__decrement_stat("bleed", -amt)

	def use_bleed(self, amt=1):
		self.__decrement_stat("bleed", amt)

	@property
	def poison(self):
		return self.__get_status("poison")

	def stack_poison(self, amt=1):
		self.__decrement_stat("poison", -amt)

	def use_poison(self, amt=1):
		self.__decrement_stat("poison", amt)


	@property
	def sealing(self):
		return self.__get_status("sealing")

	def stack_sealing(self, amt=1):
		self.__decrement_stat("sealing", -amt)

	def use_sealing(self, amt=1):
		self.__decrement_stat("sealing", amt)


	@property
	def stun(self):
		return self.__get_status("stun")

	def stack_stun(self, amt=1):
		self.__decrement_stat("stun", -amt)

	def use_stun(self, amt=1):
		self.__decrement_stat("stun", amt)


	@property
	def invis(self):
		return self.__get_status("invis")

	def stack_invis(self, amt=1):
		self.__decrement_stat("invis", -amt)

	def use_invis(self, amt=1):
		self.__decrement_stat("invis", amt)

	@property
	def encourage(self):
		return self.__get_status("encourage")

	def stack_encourage(self, amt=1):
		self.__decrement_stat("encourage", -amt)

	def use_encourage(self, amt=1):
		self.__decrement_stat("encourage", amt)

	@property
	def charm(self):
		return self.__get_status("charm")

	def stack_charm(self, amt=1):
		self.__decrement_stat("charm", -amt)

	def use_charm(self, amt=1):
		self.__decrement_stat("charm", amt)

	def get_taunt_target(self):
		v = self.__conn.execute(f"""
			select taunt from status where username="{self.__name}"
		""").fetchone()

		return v if v is None else v[0]

	def taunt_target(self, target):
		self.__conn.execute(f"""
			UPDATE status
			SET taunt="{target.label}"
			WHERE username="{self.__name}"
		""")
		self.__conn.commit()

	def end_taunt(self):
		self.__conn.execute(f"""
			UPDATE status
			SET taunt=null
			WHERE username="{self.__name}"
		""")
		self.__conn.commit()

	@property
	def label(self):
		return self.name
		

	@property
	def xp(self):
		return 0
	
	@property
	def hp(self):
		return self.health

	@property
	def max_hp(self):
		return self.max_health

	@property
	def acc(self):
		bonus = 0
		if self.accup > 0:
			bonus += 2
		if self.accdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1
		if self.poison > 0:
			acc -= 3
		return self.myclass.value.score_acc(self) + bonus
	
	@property
	def att(self):
		bonus = 0
		if self.attup > 0:
			bonus += 2
		if self.attdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1
		if self.poison >= 0:
			bonus -= 3

		return self.myclass.value.score_att(self) + bonus

	@property
	def eva(self):
		bonus = 0
		if self.evaup > 0:
			bonus += 2
		if self.evadown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1

		return self.myclass.value.score_eva(self) + bonus

	@property
	def dfn(self):
		bonus = 0

		if self.defup > 0:
			bonus += 2
		if self.defdown > 0:
			bonus -= 2
		if self.encourage > 0:
			bonus += 1

		return self.myclass.value.score_def(self) + bonus

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

	def duel_action(self, actor, party, opponents):
		return self.myclass.value.duel_action(actor, party, opponents)

	def compute_hit(self, a, d):
		return self.myclass.value.compute_hit(a, d)


	def compute_dmg(self, a, d):
		return self.myclass.value.compute_hit(a, d)

	def soulmass_count(self):
		return self.myclass.value.soulmass_count(self)

	def is_named(self, name):
		return self.name == name

	@property
	def is_player(self):
		return True

	@property
	def is_npc(self):
		return False
	





def roll_dice(amt=1, max_r=20):
	if amt < 1:
		raise ValueError(f"Amount of dice rolls must be greater than 0 (given {amt})")
	max_r = max(max_r, 1)
	return [random.randint(1, max_r) for _ in range(amt)]	


class GameManager:
	def __init__(self):
		if sys.argv[1] == "init":
			init_game_database()
			init_stats_database()

		self.__conn = get_game_database()
		self.__campaign = self.get_campaign()
		self.__campaign.restore_encounter(*self.__get_encounter())



	def __get_encounter(self):
		step = self.__conn.execute("""
				SELECT seq
				FROM sqlite_sequence
				WHERE name="encounterdata"
			""").fetchone()
		#print(step)
		#if step is None:
		#	return 
		t = self.__conn.execute(f"""
				SELECT npcs, statedata, finished
				FROM encounterdata
				ORDER BY encounterid DESC
				LIMIT 1
			""").fetchone()


		return ({}, None, True) if t is None else (npcs.string_to_npcs(t[0]), t[1], bool(t[2]))



	def __del__(self):
		self.__conn.commit()

	def start_arena(self):
		self.__conn.execute(f"""
				INSERT INTO campaigninfo (type)
				VALUES ("{Campaigns.Arena.name}")
			""")
		self.__conn.commit()

	def end_campaign(self):
		self.__conn.execute(f"""
				INSERT INTO campaigninfo (type)
				VALUES ("{Campaigns.Nothing.name}")
			""")
		self.__conn.commit()

	def get_campaign(self):
		step = self.__conn.execute("""
				SELECT seq
				FROM sqlite_sequence
				WHERE name="campaigninfo"
			""").fetchone()[0]
		t = self.__conn.execute(f"""
				SELECT type
				FROM campaigninfo
				WHERE step={step}
			""").fetchone()


		return Campaigns[t[0]].value(self.get_available_players())

	def campaign_type(self):		
		step = self.__conn.execute("""
				SELECT seq
				FROM sqlite_sequence
				WHERE name="campaigninfo"
			""").fetchone()[0]
		return Campaigns[self.__conn.execute(f"""
				SELECT type
				FROM campaigninfo
				WHERE step={step}
			""").fetchone()[0]]

	def clear_players(self):
		self.__conn.execute("""
				DELETE FROM players
			""")


	def get_available_players(self, filter=[]):
		#d = json.loads(requests.get(f"http://localhost:8911/api/chat/users").text)

		#active = set([a["Username"] for a in d] if a["Username"] not in filter)
		#active = set(["player1", "player2", "player3", "player4", "player5"])
		#active = active.difference(filter)

		step = self.get_campaign_id()
		avail = set(self.__conn.execute(f"""
				SELECT username
				FROM players
			""").fetchall())

		#return active.intersection(avail)
		return set(User(p[0]) for p in avail)

	def get_campaign_id(self):
		return self.__conn.execute("""
				SELECT seq
				FROM sqlite_sequence
				WHERE name="campaigninfo"
			""").fetchone()[0]

	def is_joined(self, user):
		val = self.__conn.execute(f"""
				SELECT username
				FROM players
				WHERE username="{user}"
			""").fetchone()

		return val is not None
		


	def join_user(self, user):
		if not isinstance(user, str):
			user = user.name
		self.__conn.execute(f"""
			INSERT OR REPLACE INTO players (username) VALUES ("{user}")
		""")
		self.__conn.commit()


	def step(self):
		self.__campaign.step()

		step = self.__conn.execute("""
				SELECT seq
				FROM sqlite_sequence
				WHERE name="encounterdata"
			""").fetchone()

		if step is None:
			self.__conn.execute(f"""
				INSERT OR REPLACE INTO encounterdata 
				(npcs, statedata, finished) 
				VALUES ("{repr(self.__campaign.npcs)}", "{repr(self.__campaign.statedata())}", {self.__campaign.finished})
			""")
		else:
			self.__conn.execute(f"""
				INSERT OR REPLACE INTO encounterdata 
				(npcs, statedata, finished) 
				VALUES ({repr(self.__campaign.npcs)}, {repr(self.__campaign.statedata())}, {self.__campaign.finished})
				WHERE encounterid={step[0]}
			""")
		self.__conn.commit()

		self.__campaign.update_interface()

	def main(self, argv):
		if argv[0] == "init":
			#init_game_database()
			#init_stats_database()
			print("Initialized Database")
		elif argv[0] == "join":
			if self.is_joined(argv[1]):
				print(f"User {argv[1]} is already part of the campaign!")
			else:
				self.join_user(argv[1])
				print(f"User {argv[1]} has joined the campaign! Make sure to choose a class and level up!")
		elif argv[0] == "startcampaign":
			ctype = Campaigns[argv[1].lower().capitalize()]
			ctype_check = self.campaign_type()
			if ctype_check != Campaigns.Nothing:
				print("Cannot start a campaign while one is active, end the current one.")
			elif ctype == Campaigns.Arena:
				self.start_arena()
				print("An arena campaign has been started! Let the bloodshed begin!")
		elif argv[0] == "campaigntype":
			print(f"{self.campaign_type().name}")
		elif argv[0] == "updateclass":
			self.join_user(argv[1])
			User(argv[1]).updateclass(argv[2])	
		elif argv[0] == "stats":
			print(User(argv[1]).stat_string())
		elif argv[0] == "level":
			self.join_user(argv[1])
			User(argv[1]).level_up(argv[2])
		elif argv[0] == "step":
			self.step()
		elif argv[0] == "basicclassaction":
			names = map_names(argv[1:])
			u = User(names[0])
			if u.dead:
				print(f"Cannot perform a class action while dead, {u.name}")
				return
			self.join_user(names[0])
			u.myclass.value.basic_action(u, self.__campaign.players, self.__campaign.npcs)
			self.__campaign.update_interface()
		elif argv[0] == "targetclassaction":
			names = map_names(argv[1:])
			u = User(names[0])
			if u.dead:
				print(f"Cannot perform a class action while dead, {u.name}")
				return
			self.join_user(names[0])
			u.myclass.value.targeted_action(u, argv[2], self.__campaign)
			self.__campaign.update_interface()
		elif argv[0] == "foelist":
			print(f"The current remaining foes are: {self.__campaign.foe_list()}")


			


def map_names(args):
	names = []
	for n in args:
		if n[0:1] != "$":
			names.append(n.lower())
		if n[0:1] == "@":
			names.append(n[1:])

	return names

from ShrimpSouls.classes import Classes
from ShrimpSouls.campaigns import NullCampaign
from ShrimpSouls.campaigns.arena import Arena
class Campaigns(enum.Enum):
	Arena = Arena
	Nothing = NullCampaign

GAME_MANAGER = GameManager()