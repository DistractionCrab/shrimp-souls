import os
import enum
import atexit
import ShrimpSouls as ss
import persistent
from dataclasses import dataclass
import persistent.list as listing
import persistent.mapping as mapping
import ShrimpSouls.messages as messages
import ShrimpSouls.utils as utils

class BaseCampaign(persistent.Persistent):
	def __init__(self, name, players=None, npcs=None):
		self.__name = name
		self.__players = mapping.PersistentMapping() if players is None else players
		self.__npcs = mapping.PersistentMapping() if npcs is None else npcs

	def resting(self, name):
		return True

	def campinfo(self):
		return {}

	@property
	def name(self):
		return self.__name	

	def clear(self):
		self.__players.clear()
		self.__npcs.clear()

	def __contains__(self, p):
		if isinstance(p, str):
			return p in self.__players

		return p.name in self.__players

	def __getitem__(self, p):
		if isinstance(p, str):			
			return self.__players.get(p, None)
		else:
			return p

	def __delitem__(self, index):
		if isinstance(index, str):
			if index in self.__players:
				del self.__players[index]
			if index in self.__npcs:
				del self.__npcs[index]
		else:
			if index in self.__players:
				del self.__players[index.name]
			if index in self.__npcs:
				del self.__npcs[index.name]

	def broadcast(self, **kwds):
		return messages.Message(
			recv=tuple(p for p in self.players),
			**kwds)

	def step(self):
		return
		yield

	def action(self, src, msg):
		return
		yield

	def add_player(self, p):
		if p.name not in self.__players:
			self.__players[p.name] = p

		yield from self._add_player(p)

	def _add_player(self, p):
		return
		yield

	def add_npc(self, p):
		if p.name not in self.__npcs:
			self.__npcs[p.name] = p

		self._add_npc(p)

	def _add_npc(self, p):
		return 
		yield

	@property
	def players(self):
		return utils.FrozenDict(self.__players)
	
	@property
	def npcs(self):
		return utils.FrozenDict(self.__npcs)

	def opponents(self, att):
		tt = att.get_taunt_target()
		if att.is_player:
			if tt is not None:
				return [self.get_target(tt)]
			elif att.status.charm > 0:
				return self.players
			else:
				return self.npcs.values()
		else:
			if tt is not None:
				return [self.get_target(tt)]
			if att.status.charm == 0:
				return self.players.values()
			else:
				return self.npcs.values()

	def allies(self, att):
		if att.is_player:
			if att.status.charm == 0:
				return self.players.values()
			else:
				return self.npcs.values()
		else:
			if att.status.charm > 0:
				return self.players.values()
			else:
				return self.npcs.values()


	def find_valid_target(self, att, ally, aliveq, amt=1, targets=tuple(), **kwds):
		if att.status.charm == 0:
			targets = (self.get_target(n) for n in targets)
			targets = tuple(p for p in targets if p is not None and not p.dead)
		else:
			targets = tuple()

		if len(targets) >= amt:
			return targets[:amt]
		else:

			amt = amt - len(targets)
			pool = self.allies(att) if ally else self.opponents(att)
			pool = pool if not aliveq else filter(lambda x: x is not None and not x.dead, pool)
			pool = tuple(p for p in pool if p.status.invis == 0 or random.random() < 0.1)
			pool = tuple(set(random.sample(pool, k=min(amt, len(pool)))))
			return pool + targets

	def get_player(self, name):
		return self.__players[name] if name in self.__players else None

	def get_npc(self, name):
		return self.__npcs[name] if name in self.__npcs else None

	def get_target(self, t):
		t1 = self.get_player(t)
		if t1 is None:
			t1 = self.get_npc(t)

		return t1


	def use_ability(self, p, abi, targets):
		yield messages.Message(
			msg=(f"Cannot use abilities in {type(self)}",),
			recv=(p.name,))
