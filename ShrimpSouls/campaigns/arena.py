import random
import os
from functools import reduce
from ShrimpSouls import npcs
from ShrimpSouls.logger import log

import os
import diskcache as dc
import ShrimpSouls as ss

CACHE_DIR = ss.CACHE_DIR/"campaigns"/"arena"
CACHE = dc.Cache(CACHE_DIR)


if 'players' not in CACHE:
	CACHE['players'] = []
if 'npcs' not in CACHE:
	CACHE['npcs'] = []

def reset_combatants():
	CACHE['npcs'] = []
	CACHE['players'] = []


class Arena:
	def __init__(self):
		self.__players = None
		self.__npcs = None

	@property
	def players(self):
		if self.__players is None:
			self.__players = list([ss.get_player(p) for p in CACHE['players']])

		return self.__players
	
	@property
	def npcs(self):
		if self.__npcs is None:
			self.__npcs = list(CACHE['npcs'])

		return self.__npcs

	@property
	def start_msg(self):
		return "An Arena has started! !join the arena to fight powerful foes!"

	def join(self, player):
		if any(player == p.name for p in self.players):
			print(f"{player} is already in the arena!")
		else:
			p = CACHE['players']
			p.append(player)
			CACHE['players'] = p
			print(f"{player} has joined the arena! ")
			if not self.finished:
				player = ss.get_player(player)
				npcs = self.__add_foes(player)
				fstring = (f.name for f in npcs)
				print(f"As {player.name} joines the arena so do {', '.join(fstring)}")

			self.commit()

		

	def step(self):
		#print(self.npcs)
		if len(self.players) == 0:
			print("No players available for the arena: type !join to join the campaign!")
		elif self.finished:
			print("The arena has begun!")
			self.__setup_arena()			
		else:
			self.__do_combat()
			self.commit()

		

	def commit(self):
		for p in self.players:
			p.commit()
		CACHE['npcs'] = list(n for n in self.npcs)

	def __find_appropriate_encounter(self):
		avg = int(sum(p.level for p in self.players)/len(self.players))
		try:
			k = next(k for k in ENCOUNTERS.keys() if avg in k)
			(l, m) = random.choices(ENCOUNTERS[k])[0]
			return l(len(self.players)), m
		except StopIteration:
			(l, m) = (
				lambda n: npcs.Goblin.generate(3*n),
				"Many Goblins"
			)

			return l(len(self.players)), m

	def __setup_arena(self):
		self.__npcs = []
		
		for p in self.players:
			p.revive()
			p.reset_status()

			self.__add_foes(p)	

		self.commit()
		self.foes()

	def __add_foes(self, p):
		k = next(k for k in ENCOUNTERS.keys() if p.level in k)
		foes = random.choices(ENCOUNTERS[k])[0](len(self.npcs))
		for n in foes:
			self.npcs.append(n)

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

		print(msg)
		log("------------------------------------------------------------")

		if self.finished:
			reset_combatants()


		
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


	def get_player(self, name):
		return next(p for p in self.players if p.name == name)

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
		foes = self.npcs
		if len(foes) == 0:
			print("No enemies can be seen...")
		else:
			valid = list(filter(lambda x: not x.dead, foes))
			f = set(random.choices(valid,k=5))

			fstrings = (f'{n.name}({n.hp}/{n.max_hp})' for n in f)
			print(f"Some foes you can see: {', '.join(fstrings)}")





ENCOUNTERS = {
	range(1, 6): [
		lambda i: npcs.Goblin.generate(3, i),
		lambda i: npcs.Wolf.generate(2, i),
	],
	range(5, 13): [
		lambda i: npcs.GoblinBrute.generate(2, i)
		lambda i: npcs.GoblinBrute.generate(1, i) + npcs.GoblinPriest.generate(1, i)
	]
}
