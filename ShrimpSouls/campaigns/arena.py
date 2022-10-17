import random
import os
from functools import reduce
from ShrimpSouls import npcs
from ShrimpSouls.logger import log

import os
import atexit
import diskcache as dc
import ShrimpSouls as ss

CACHE_DIR = ss.CACHE_DIR/"campaigns"/"arena"
PLAYERS = dc.Cache(CACHE_DIR/"players")
ENEMIES = dc.Cache(CACHE_DIR/"enemies")

def add_npc(n):
	ENEMIES[n.name] = n

def reset_combatants():
	for p in PLAYERS:
		p = ss.get_player(p)
		p.reset_status()
		p.revive()
	PLAYERS.clear()
	ENEMIES.clear()
	#print("resetting.")

_MODIFIED = set()

def commit_npc(self):
	if not self.dead:
		_MODIFIED.update([self])
	else:
		del ENEMIES[self.name]

def save_npcs():
	for n in _MODIFIED:
		if n.name in ENEMIES and not n.dead:
			ENEMIES[n.name] = n



class Arena:
	def __init__(self):
		self.__npcs = list(ENEMIES[n] for n in ENEMIES)
		self.__players = list(ss.get_player(p) for p in PLAYERS)


	@property
	def players(self):
		return (a for a in self.__players)
	
	@property
	def npcs(self):
		return (a for a in self.__npcs)



	@property
	def start_msg(self):
		return "An Arena has started! !join the arena to fight powerful foes!"

	def join(self, player):
		player = ss.get_player(player)
		if player.name in PLAYERS:
			print(f"{player.name} is already in the arena! ")
		else:
			
			PLAYERS[player.name] = None

			print(f"{player.name} has joined the arena! ")
			if not self.finished:
				npcs = self.__add_foes(player)
				#print(npcs)
				fstring = (f.name for f in npcs)
				print(f"As {player.name} joins the arena so do {', '.join(fstring)} ")

			self.commit()

		

	def step(self):
		if len(PLAYERS) == 0:
			print("No players available for the arena: type !join to join the campaign!")
		elif len(ENEMIES) == 0:
			print("The arena has begun!")
			self.__setup_arena()			
		else:
			self.__do_combat()
			self.commit()

		

	def commit(self):
		for p in self.__players:
			if p.dead:
				del PLAYERS[p.name]
		for p in self.__npcs:
			if p.dead:
				del ENEMIES[p.name]
			else:
				ENEMIES[p.name] = p

	def __find_appropriate_encounter(self):
		players = list(self.players)
		avg = int(sum(p.level for p in players)/len(players))
		try:
			k = next(k for k in ENCOUNTERS.keys() if avg in k)
			(l, m) = random.choices(ENCOUNTERS[k])[0]
			return l(len(players)), m
		except StopIteration:
			(l, m) = (
				lambda n: npcs.Goblin.generate(3*n),
				"Many Goblins"
			)

			return l(len(self.players)), m

	def __setup_arena(self):
		npcs = []
		#ENEMIES.clear()
		#PLAYERS.clear()
		
		for p in self.players:
			p.revive()
			p.reset_status()

			self.__add_foes(p)	

		self.commit()
		self.foes()

	def __add_foes(self, p):
		k = next(k for k in ENCOUNTERS.keys() if p.level in k)
		foes = random.choices(ENCOUNTERS[k])[0](len(ENEMIES))
		for n in foes:
			self.__npcs.append(n)

		return foes

	def __do_combat(self):
		order = list(self.players) + list(self.npcs)
		order = list(filter(lambda x: not x.dead and x.stun <= 0, order))
		random.shuffle(order)



		p_fetch = lambda x: self.players if x in self.players else self.npcs
		o_fetch = lambda x: self.npcs if x in self.players else self.players
		#actions =  [p.duel_action(p, p_fetch(p), o_fetch(p)) for p in order if not p.stun > 0]
		#actions =  [self.get_action(p) for p in order if  p.stun <= 0]
		#actions = reduce(lambda a, b: a + b, actions, [])
		for p in order:
			p.tick()

		alivep = [p for p in self.players if not p.dead]
		aliven = [p for p in self.npcs if not p.dead]

		for p in order:
			#log(f"Getting actions for {p.label}")
			if self.finished:
				break
			actions = self.get_action(p)
			#log(f"{p.label}'s actions: {actions}")
			for a in actions:
				a.apply()
				if p.is_player:
					log("---" + a.msg)
				else:
					log(a.msg)
				if self.finished:
					break


		msg = ""

		dead = [p for p in alivep if p.dead]

		if len(dead) > 0 and len(dead) <= 3:
			msg += f"{', '.join(p.name for p in dead)} have perished in the arena. "
		elif len(dead) > 0:
			msg += "Many players have perished in the arena. "


		dead1 = [p for p in aliven if p.dead]

		if len(dead1) > 0:
			if len(dead1) <= 3:
				msg += f"{', '.join(p.name for p in dead1)} have perished in the arena. "
			else:
				msg += "Many foes have perished in the arena. "

			xp = sum(p.xp for p in dead1)
			for p in self.players:
				p.add_shrimp(xp)

			msg += f"The party gains {xp} shrimp. "
			

		if len(dead) == 0 and len(dead1) == 0:
			msg += "No deaths so far."

		if not self.finished:
			msg += f"The battle, however, continues to rage..."
		else:
			if all(p.dead for p in self.players):
				msg += "The match has ended. The party has been defeated..."
			elif all(p.dead for p in self.npcs):
				msg += f"The match has ended. The party is victorious!!!"


		# Handle ticking for buffs/debuffs.
		order = list(self.players) + list(self.npcs)
		order = list(filter(lambda x: not x.dead, order))

		for p in order:
			p.tick()

		print("**The Turn has Ended**: " + msg)
		log("------------------------------------------------------------")

		for p in self.players:
			p.allow_actions()

		#self.commit()

		
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

	@property
	def finished(self):
		return all(p.dead for p in self.players) or all(p.dead for p in self.npcs)

	def foes(self):
		if len(ENEMIES) == 0:
			print("No enemies can be seen...")
		else:
			#print(self.__npcs)
			valid = list(filter(lambda x: not x.dead, self.npcs))
			if len(valid) == 0:
				print("All foes are dead.")
				return
			f = set(random.choices(valid,k=5))

			fstrings = (f'{n.name}({n.hp}/{n.max_hp})' for n in f)
			print(f"Some foes you can see: {', '.join(fstrings)}")

	def perform_action(self, pname):
		if pname.lower() not in PLAYERS:
			print(f"{u.name} is not in the campaign. !join to perform an action.")
		else:
			p = ss.get_player(pname)
			if p.acted:
				print(f"{p.name} has already acted this turn.")
			else:				
				actions = p.act(self)
				for a in actions:
					a.apply()
					print(a.msg)

				p.did_act()
		self.commit()

	def perform_target_action(self, pname, target):
		if pname.lower() not in PLAYERS:
			print(f"{u.name} is not in the campaign. !join to join!")
		else:
			p = ss.get_player(pname)
			if p.acted:				
				print(f"{p.name} has already acted this turn.")
			else:				
				t = self.get_target(target)
				actions = p.target(t, self)
				for a in actions:
					a.apply()
					print(a.msg)

				p.did_act()

				if t.dead:
					print(f"{t.name} has died.")
					if not t.is_player:
						for p in self.players:
							p.add_shrimp(t.xp)
						if len(ENEMIES) == 0:
							print("All enemies have been defeated and the arena is over.")
							PLAYERS.clear()
		self.commit()






ENCOUNTERS = {
	range(1, 6): [
		lambda i: npcs.Goblin.generate(3, i),
		lambda i: npcs.Wolf.generate(2, i),
	],
	range(5, 13): [
		lambda i: npcs.GoblinBrute.generate(1, i),
		lambda i: (
			npcs.GoblinBrute.generate(1, i) 
			+ npcs.GoblinPriest.generate(1, i) if (random.uniform(0, 1) < 0.5) else [])
	]
}
