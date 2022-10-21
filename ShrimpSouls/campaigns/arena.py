import random
import os
from functools import reduce
from ShrimpSouls import npcs
from ShrimpSouls.logger import log
import ShrimpSouls.utils as utils

import os
import atexit
import diskcache as dc
import ShrimpSouls as ss

CACHE_DIR = ss.CACHE_DIR/"campaigns"/"arena"
PLAYERS = dc.Cache(CACHE_DIR/"players")
ENEMIES = dc.Cache(CACHE_DIR/"enemies")


class ArenaBase:
	def __init__(self):		
		self.__player_list = None


	@property
	def players(self):
		return utils.ListGuard(self.__players)
	


	def add_player(self, p):
		if isinstance(p, str):
			p = ss.get_player(p)

		self.__players.append(p)
		PLAYERS[p.name] = None

	

	@property
	def __players(self):
		if self.__player_list is None:
			self.__player_list = list(ss.get_player(p) for p in PLAYERS)
		return self.__player_list

	def join(self, player):
		player = ss.get_player(player)
		if player.name in PLAYERS:
			print(f"{player.name} is already in the arena! ")
		else:
			player.revive()
			player.reset_status()
			player.allow_actions()
			PLAYERS[player.name] = None

			print(f"{player.name} has joined the arena! They have been healed and refreshed.")


	def perform_action(self, pname):		
		print("No actions to be performed in arena setup")
		return "No actions to be performed in arena setup"

	def perform_target_action(self, pname, target):
		print("No actions to be performed in arena setup")
		return "No actions to be performed in arena setup"


	def foes(self):
		print("No foes exist in the arena waiting room; Here have a cup of tea.")
		return "No foes exist in the arena waiting room; Here have a cup of tea."


	def get_player(self, name):
		return next(p for p in self.players if p.name.lower() == name.lower())

	def get_enemy(self, name):
		return next(p for p in self.npcs if p.labeled(name))

	def get_target(self, name):
		try:
			return self.get_player(name)
		except StopIteration:
			try:
				return self.get_enemy(name)
			except StopIteration:
				raise ValueError(f"No player or npc named {name}")

	def enter(self, previous):
		return ''

	def exit(self):
		return ''

	def close(self):
		pass


class Setup(ArenaBase):
	def step(self):
		import ShrimpSouls.campaigns as cps	
		if len(PLAYERS) == 0:
			print("No players available for the arena: type !join to join the campaign!")
			return (cps.Campaigns.ArenaSetup, "No players available for the arena: type !join to join the campaign!")
		else:			
			return (cps.Campaigns.Arena, "")

	@property
	def start_msg(self):
		return "The arena is setting up, !join to make sure you're in the arena."


	def get_player(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_enemy(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_target(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def enter(self, previous):
		print("The Arena is getting setup, make sure to !join")
		import ShrimpSouls.campaigns as cps
		if previous != cps.Campaigns.Arena:
			PLAYERS.clear()
		return "The Arena is getting setup, make sure to !join"


class Arena(ArenaBase):
	def __init__(self):
		super().__init__()
		self.__npc_list = None

	def join(self, player):
		player = ss.get_player(player)
		if player.name in PLAYERS:
			print(f"{player.name} is already in the arena! ")
			return f"{player.name} is already in the arena! "
		else:
			player.revive()
			player.reset_status()
			self.add_player(player)

			msg = f"{player.name} has joined the arena! "
			if not self.finished:
				npcs = self.__add_foes(player)
				#print(npcs)
				fstring = (f.name for f in npcs)
				msg += f"As {player.name} joins the arena so do {', '.join(fstring)} "
			print(msg)
			return msg

	def close(self):
		n = list(ENEMIES)
		e = [e.name for e in self.__npcs]
		d = [v for v in n if v not in e]

		for name in d:
			del ENEMIES[name]

		for e in self.__npcs:
			ENEMIES[e.name] = e

	@property
	def npcs(self):
		return utils.ListGuard(self.__npcs)

	def add_npc(self, n):
		self.__npcs.append(n)

	def clear_npcs(self):
		self.__npc_list = []

	@property
	def __npcs(self):
		if self.__npc_list is None:
			self.__npc_list = list(ENEMIES[n] for n in ENEMIES)

		return self.__npc_list

	def enter(self, previous):
		import ShrimpSouls.campaigns as cps
		if previous == cps.Campaigns.ArenaSetup:
			print("The Arena has started!!!")
			self.__setup_arena()
			return "The Arena has started!!!"
		else:
			PLAYERS.clear()
			ENEMIES.clear()
			return "The Arena is getting setup."

		return ''

		

	def exit(self):
		for p in self.players:
			p.revive()
			p.reset_status()
			p.allow_actions()

		ENEMIES.clear()
		self.clear_npcs()

		return ''

	@property
	def start_msg(self):
		return "An Arena has started! !join the arena to fight powerful foes!"
		

	def step(self):
		import ShrimpSouls.campaigns as cps

		#print(self.npcs)
		#print(self.players)
		if len(self.npcs) == 0 or len(self.players) == 0:
			print("Is this happening?")
			return (cps.Campaigns.ArenaSetup, '')
		
		msg = self.__do_combat()

		if self.finished:
			return (cps.Campaigns.ArenaSetup, msg)
		else:
			return (cps.Campaigns.Arena, msg)

	
	def __setup_arena(self):
		for p in self.players:
			p.revive()
			p.reset_status()
			p.allow_actions()

		
			f = self.__add_foes(p)	
			#print(f"Foes added for {p.name} = {[f.name for f in f]}")

		self.foes()

	def __add_foes(self, p):
		k = next(k for k in ENCOUNTERS.keys() if p.level in k)
		foes = random.choices(ENCOUNTERS[k])[0](len(self.npcs))
		#print(f"foes = {[f.name for f in foes]}")
		for n in foes:
			self.add_npc(n)


		return foes

	def __do_combat(self):
		ignore_round_print = not self.finished
		party = set(self.players)
		enemies = set(self.npcs)

		order = list(a for a in party.union(enemies) if not a.dead)
		random.shuffle(order)

		#for p in order:
		#	p.tick()

		alivep = [p for p in party if not p.dead]
		aliven = [p for p in enemies if not p.dead]

		for p in order:
			if self.finished:
				break
			if p.stun == 0:
				actions = self.get_action(p)
				for a in actions:
					a.apply()
					log(a.msg)

			#if not p.is_player:
			#	p.damage(p.hp)
			else:
				log(f"{p.name} was stunned and couldn't act.")


		msg = self.__get_death_msgs(alivep, aliven, ignore_round_print)


		for p in order:
			if not p.dead:
				p.tick()

		#msg = "**The Turn has Ended**: " + msg
		log("------------------------------------------------------------")

		for p in self.players:
			p.allow_actions()

		print(msg)
		return msg

	def handle_dead_foes(self):
		s = 0
		for n in self.npcs:			
			if n.dead:
				s += n.xp
				n.xp = 0

		if s > 0:
			return f"The party has been awarded {s} xp."
		else:
			return ''



	def __get_death_msgs(self, party, enemies, ignore_round_print):
		msg = ""

		deadp = [p for p in party if p.dead]
		deade = [p for p in enemies if p.dead]

		if len(deadp) > 0 and len(deadp) <= 3:
			msg += f"{', '.join(p.name for p in deadp)} have perished in the arena. "
		elif len(deadp) > 0:
			msg += "Many players have perished in the arena. "
		

		if len(deade) > 0:
			if len(deade) <= 3:
				msg += f"{', '.join(p.name for p in deade)} have perished in the arena. "
			else:
				msg += "Many foes have perished in the arena. "

			msg += self.handle_dead_foes()
			

		if len(deadp) == 0 and len(deade) == 0 and not ignore_round_print:
			msg += "No deaths so far..."

		if not self.finished:
			msg += f"The battle, however, continues to rage..."
		else:
			if all(p.dead for p in self.players):
				msg += "The match has ended. The party has been defeated..."
			elif all(p.dead for p in self.npcs):
				msg += f"The match has ended. The party is victorious!!!"

			

		return msg

		
	def get_action(self, entity):
		tt = entity.get_taunt_target()
		if entity.is_player:
			if tt is not None:
				return entity.duel_action(entity, self.players, [self.get_target(tt)])
			elif entity.charm > 0:
				return entity.duel_action(entity, self.npcs, self.players)			
			else:
				return entity.duel_action(entity, self.players, self.npcs)
		else:
			if tt is not None:
				return entity.duel_action(entity, self.npcs, [self.get_target(tt)])
			elif entity.charm > 0:
				return entity.duel_action(entity, self.players, self.npcs)
			else:
				return entity.duel_action(entity, self.npcs, self.players)

	def is_joined(self, name):
		return name in CACHE['players']



	@property
	def finished(self):
		return all(p.dead for p in self.players) or all(p.dead for p in self.npcs)

	

	def perform_action(self, pname):
		
		if pname.lower() not in PLAYERS:
			print(f"{pname} is not in the campaign. !join to perform an action.")		
		else:
			p = ss.get_player(pname)
			if p.acted:
				print(f"{p.name} has already acted this turn.")
				return f"{p.name} has already acted this turn."
			elif p.dead:
				print(f"{p.name} cannot perform actions while dead.")
				return f"{p.name} cannot perform actions while dead."
			elif p.status.stun > 0:
				print(f"{p.name} cannot perform actions while stunned.")
				return f"{p.name} cannot perform actions while stunned."
			else:
				msg = ''		
				actions = p.act(self)
				for a in actions:
					a.apply()
					msg += a.msg

				p.did_act()

				msg += self.handle_dead_foes()

				print(msg)
				return msg


	def perform_target_action(self, pname, target):
		if pname.lower() not in PLAYERS:
			print(f"{pname} is not in the campaign. !join to join!")
		else:
			p = ss.get_player(pname)
			if p.acted:				
				print(f"{p.name} has already acted this turn.")
			elif p.dead:
				print(f"{p.name} cannot perform actions while dead.")
			elif p.status.stun > 0:
				print(f"{p.name} cannot perform actions while stunned.")
			else:
				msg = ''
				if target == "me":
					t = p
				else:		
					t = self.get_target(target)
				actions = p.target(t, self)
				for a in actions:
					a.apply()
					msg += a.msg

				p.did_act()

				msg += self.handle_dead_foes()

				print(msg)
				return msg


	def foes(self):
		if len(self.npcs) == 0:
			print("No enemies can be seen...")
		else:
			#print(self.__npcs)
			valid = list(filter(lambda x: not x.dead, self.__npcs))
			if len(valid) == 0:
				print("All foes are dead.")
				return
			f = set(random.sample(valid,k=min(5, len(valid))))

			fstrings = (f'{n.name}({n.hp}/{n.max_hp})' for n in f)
			print(f"Some foes you can see: {', '.join(fstrings)}")








ENCOUNTERS = {
	range(1, 5): [
		lambda i: npcs.Goblin.generate(1, i),
		lambda i: npcs.Wolf.generate(1, i),
	],
	range(5, 10): [
		lambda i: npcs.GoblinBrute.generate(2, i),
		lambda i: (
			npcs.GoblinBrute.generate(1, i) 
			+ (npcs.GoblinPriest.generate(1, i) if (random.uniform(0, 1) < 0.5) else tuple())),
	],

	range(10, 15): [
		lambda i: npcs.OrcWarrior.generate(3, i),
		lambda i: (
			npcs.OrcWarrior.generate(2, i) 
			+ (npcs.GoblinPriest.generate(1, i) if (random.uniform(0, 1) < 0.5) else tuple())),
		lambda i: npcs.Ogre.generate(1, i),
	]
	
}

