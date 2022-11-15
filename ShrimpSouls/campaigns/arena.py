import random
import os
import persistent
import persistent.list
import persistent.mapping
from functools import reduce
from ShrimpSouls import npcs

import ShrimpSouls.utils as utils

import os
import atexit
import ShrimpSouls as ss
import ShrimpSouls.messages as messages

def refresh_player(p):
	p.revive()
	p.reset_status()


class BaseArena(persistent.Persistent):
	def __init__(self, players=None):
		if players is None:
			self.__players = persistent.mapping.PersistentMapping()
		else:
			self.__players = players


	def get_player(self, name):
		if isinstance(name, str):
			if name in self.__players:
				return self.__players[name]
			else:
				return None
		else:
			if name.is_player:
				return name
			else:
				return None

	@property
	def restarea(self):
		return False
	

	def get_npc(self, name):
		return None
		

	@property
	def players(self):
		return self.__players

	@property
	def npcs(self):
		return {}
	
	def is_joined(self, name):	
		if isinstance(name, str):
			return name in self.__players
		else:
			return name.name in self.__players


	def add_player(self, p):
		self.__players[p.name] = p

	def join(self, player):
		if player.name in self.__players:
			return f"{player.name} is already in the arena! "
		else:
			player.revive()
			player.reset_status()
			self.add_player(player)

			msg = f"{player.name} has joined the arena! "
			return msg

	@property
	def npcs(self):
		return {}

	def add_npc(self, n):
		pass

	def clear_npcs(self):
		pass

	def clear_players(self):
		self.__players.clear()

	@property
	def player_ct(self):
		return len(self.__players)

	def __contains__(self, a):
		if isinstance(a, str):
			return a in self.__players

		else:
			return a.name in self.__players

	

class WaitingRoom(BaseArena):
	def __init__(self, players=None):
		super().__init__(players=players)
		self.ct = 0

	@property
	def restarea(self):
		return True


	def step(self):
		if self.player_ct == 0:
			return (self, messages.Message(msg=["No players in the arena, click Join to join!"]))
		else:
			for p in self.players.values():
				refresh_player(p)
			return (
				Arena(self.players), 
				messages.Message(
					msg=["The Arena is starting soon..."],
					users=list(self.players.values())))
				



	def use_ability(self, p, abi, targets):
		return messages.Error(msg=["Cannot use abilities in rest areas."])



class Arena(BaseArena):
	def __init__(self, players=None):
		super().__init__(players=players)
		self.__npcs = persistent.mapping.PersistentMapping()		
	

	def get_npc(self, name):
		if isinstance(name, str):
			if name in self.__npcs:
				return self.__npcs[name]
			else:
				return None
		else:
			return name

	@property
	def npc_ct(self):
		return len(self.__npcs)


	def join(self, player):
		if self.is_joined(player):
			return f"{player.name} is already in the arena! "
		else:
			player.revive()
			player.reset_status()
			self.add_player(player)

			msg = f"{player.name} has joined the arena! "
			if not self.finished:
				npcs = self.__add_foes(player)				
				if len(npcs) > 0:
					fstring = (f.name for f in npcs)
					msg += f"As {player.name} joins the arena so do {', '.join(fstring)} "
			return msg

	@property
	def npcs(self):
		return self.__npcs

	def add_npc(self, n):
		self.__npcs[n.name] = n

	def clear_npcs(self):
		self.__npcs.clear()

		

	def step(self):
		if self.player_ct == 0:
			return (self, messages.Message(msg=["No players available, click Join to participate!"]))
		elif len(self.__npcs) == 0:
			while len(self.__npcs) == 0:
				self.__setup_arena()
			return (self, messages.Message(
				msg=["The Arena has started!!!"],
				users=list(self.players.values()),
				npcs=list(self.npcs.values()),
				refreshEntities=True))
		else:
			v = self.__do_combat()
			if self.finished:
				return (WaitingRoom(self.players), v)
			else:
				return (self, v)

	
	def __setup_arena(self):
		for p in self.players.values():
			p.revive()
			p.reset_status()
			p.allow_actions()

		
			f = self.__add_foes(p)	
			#print(f"Foes added for {p.name} = {[f.name for f in f]}")
		#print(self.foes())


	def __add_foes(self, p):
		k = next(k for k in ENCOUNTERS.keys() if p.level in k)
		foes = random.choices(ENCOUNTERS[k])[0](len(self.__npcs))
		#print(f"foes = {[f.name for f in foes]}")
		for n in foes:
			self.add_npc(n)


		return foes

	def __do_combat(self):
		party = list(self.players.values())
		enemies = list(self.npcs.values())

		order = list(a for a in (party + enemies) if not a.dead)
		random.shuffle(order)


		rec_p = set()
		rec_n = set()
		total = []

		for p in order:
			if self.finished:
				break
			if p.stun == 0:
				actions = p.duel_action(self)
				if not p.acted:
					ract = p.random_action(p, self)
					if ract is None:
						print(f"None action for {p.name}")
						ract = []
					if actions is None:
						print(f"None actions for {p.name}")
						actions = []
					actions = ract + actions
				for a in actions:
					a.apply()
					total.append(a.msg + " " + self.handle_dead_foes(a.receivers_npc))
					rec_p.update(a.receivers)
					rec_n.update(a.receivers_npc)



		for p in order:
			if not p.dead:
				p.tick()

		for p in self.players.values():
			p.allow_actions()

		f = self.finished 

		if f:
			if all(p.dead for p in self.players.values()):
				total.append("The party has been defeated...")
			if all(p.dead for p in self.npcs.values()):
				total.append("The party is Victorious!!!")
		else:
			total.append("The battle continues to rage.")


		if f:
			return messages.Message(
				msg=total, 
				users=rec_p, 
				npcs=rec_n, 
				remove_npc=list(self.__npcs.keys()))
		else:
			return messages.Message(msg=total, users=rec_p, npcs=rec_n)

	

	def handle_dead_foes(self, rec_n):
		if len(rec_n) == 0:
			return ''

		d = []
		s = 0
		for n in rec_n:
			if n.dead and n.xp > 0:
				d.append(n)
				s += n.xp
				n.xp = 0

		for p in self.players.values():
			p.add_shrimp(s)

		if len(d) > 0:
			if len(d) > 3:
				return f"Many foes have fallen. The party has been awarded {s} xp."
			else:
				return f"{', '.join(n.name for n in d)} have fallen. The party has been awarded {s} xp."
			
		else:
			return ''


		
	def get_action(self, entity):
		tt = entity.get_taunt_target()
		if entity.is_player:
			if tt is not None:
				return entity.duel_action(entity, self)
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


	@property
	def finished(self):
		return all(p.dead for p in self.players.values()) or all(p.dead for p in self.npcs.values())


	def opponents(self, att):
		tt = att.get_taunt_target()
		if att.is_player:
			if tt is not None:
				return [self.get_target(tt)]
			elif att.charm > 0:
				return self.players
			else:
				return self.npcs.values()
		else:
			if tt is not None:
				return [self.get_target(tt)]
			if att.charm == 0:
				return self.players.values()
			else:
				return self.npcs.values()

	def allies(self, att):
		if att.is_player:
			if att.charm == 0:
				return self.players.values()
			else:
				return self.npcs.values()
		else:
			if att.charm > 0:
				return self.players.values()
			else:
				return self.npcs.values()

	def get_target(self, t):
		t1 = self.get_player(t)
		if t1 is None:
			t1 = self.get_npc(t)

		return t1


	@property
	def front_line(self):
		return list(p for p in self.players.values() if p.position == ss.Positions.FRONT)

	@property
	def back_line(self):
		return list(p for p in self.players.values() if p.position == ss.Positions.BACK)

	def find_valid_target(self, att, ally, pos, aliveq, amt=1):
		pool = self.allies(att) if ally else self.opponents(att)
		pool = pool if not aliveq else list(filter(lambda x: not x.dead, pool))
		pool = list(filter(
			lambda x: x.position in pos or x.invis > 0 or all(p.dead for p in self.front_line), 
			pool))
		pool = list(set(random.sample(pool, k=min(amt, len(pool)))))

		return pool

	def use_ability(self, p, abi, targets):
		if not self.is_joined(p.name):
			return messages.Error(msg=[f"{p.name} is not in the campaign. !join to join!"])
		else:
			if p.acted:				
				return messages.Error(msg=[f"{p.name} has already acted this turn."])
			elif p.dead:
				return messages.Error(msg=[f"{p.name} cannot perform actions while dead. Deadge"])
			elif p.status.stun > 0:
				return messages.Error(msg=[f"{p.name} cannot perform actions while stunned."])
			else:
				try:
					rec = set()
					rec_n = set()
					total = []
					targets = list(filter(lambda x: x is not None, [self.get_target(t) for t in targets]))
					actions = p.myclass.use_ability(p, abi, targets, self)
					#print(actions)
					for a in actions:
						a.apply()
						total.append(a.msg)
						dd = self.handle_dead_foes(a.receivers_npc)
						if len(dd) > 0:
							total.append(dd)
						rec.update(a.receivers)
						rec_n.update(a.receivers_npc)

					p.did_act()
					return messages.Message(msg=total, users=rec, npcs=rec_n)
				except Exception as ex:
					raise ex
					return messages.Error(msg=[str(ex)])


	def foes(self):
		if len(self.npcs) == 0:
			return "No enemies can be seen..."
		else:
			#print(self.__npcs)
			valid = list(filter(lambda x: not x.dead, self.__npcs.values()))
			if len(valid) == 0:
				return "All foes are dead."
				return
			f = set(random.sample(valid,k=min(5, len(valid))))

			fstrings = (f'{n.name}({n.hp}/{n.max_hp})' for n in f)
			return f"Some foes you can see: {', '.join(fstrings)}"







ENCOUNTERS = {
	range(1, 5): [
		lambda i: npcs.Goblin.generate(3, i, prob=0.7),
		lambda i: npcs.Wolf.generate(2, i, prob=0.6),
	],
	range(5, 10): [
		lambda i: npcs.GoblinBrute.generate(2, i, prob=0.6),
		lambda i: npcs.GoblinBrute.generate(1, i) + npcs.GoblinPriest.generate(1, i, prob=0.7) ,
	],

	range(10, 15): [
		lambda i: npcs.OrcWarrior.generate(2, i, prob=0.5),
		lambda i: npcs.OrcWarrior.generate(1, i) + npcs.GoblinPriest.generate(2, i, prob=0.5),
		lambda i: npcs.Ogre.generate(2, i, prob=0.6),
		
	],
	range(15, 21): [
		lambda i: npcs.Troll.generate(1, i, prob=0.5),
		lambda i: npcs.Wraith.generate(1, i),
	],
	range(21, 200): [
		lambda i: npcs.OxTitan.generate(1, i, prob=0.005),
		lambda i: npcs.BloodGolem.generate(1, i, prob=0.5),
	],
}
