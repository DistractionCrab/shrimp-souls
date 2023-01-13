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

	def __contains__(self, p):
		if isinstance(p, str):
			return p in self.__players

		return p.name in self.__players

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

	def find_valid_target(self, att, dfn, evn, **kwds):
		return tuple()

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
