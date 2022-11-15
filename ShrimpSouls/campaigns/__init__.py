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

	def location(self, p):
		if p.name in self.__players:
			return self
		else:
			return None

	def resting(self, name):
		if name in self.__players:
			return self.restarea
		else:
			None


	@property
	def areaname(self):
		return "Unnamed Area - BaseCampaign"	

	@property
	def name(self):
		return self.__name

	def resides(self, p):
		return p in self
	

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
			recv=tuple(p for p in self.players if self.resides(p)),
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

		self._add_player(p)

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
	def finished(self):
		return False	

	@property
	def players(self):
		return utils.FrozenDict(self.__players)
	
	@property
	def npcs(self):
		return utils.FrozenDict(self.__npcs)

	def find_valid_target(self, att, dfn, evn, pos, amt=1):
		return tuple()

	def get_npc(self, name):
		return None


	def use_ability(self, p, abi, targets):
		yield messages.Respond(msg=(f"Cannot use abilities in {type(self)}",))

	@property
	def restarea(self):
		return True


class RootCampaign(BaseCampaign):
	def __init__(self, name, players=None, npcs=None):
		super().__init__(name)
		self.__subs = mapping.PersistentMapping()

	def __setitem__(self, index, value):
		self.__subs[index] = value

	def __getitem__(self, index):
		return self.__subs[index]

	def __delitem__(self, index):
		if isinstance(index, str):
			if index in self.__subs:
				del self.__subs[index]
		super().__delitem__(index)


	def __len__(self):
		return len(self.__subs)

	def step(self):
		yield from self._step()
		for s in self.__subs:
			yield from s.step()

	def _step(self):
		return
		yield

	def use_ability(self, p, abi, targets):
		if self.resides(p):
			yield from self._use_ability(p, abi, targets)
		else:
			for s in self.__subs.values():
				if src in s:
					yield from s.use_ability(p, abi, targets)

		

	def _use_ability(self, p, abi, targets):
		return
		yield

	@property
	def act_always(self):
		return False

	def action(self, src, msg):
		if self.resides(src):
			yield from self._action(msg)
		else:
			if self.act_always:
				yield from self._action(msg)
			for s in self.__subs.values():
				if src in s:
					yield from s.action(src, msg)

		

	def _action(self, arc, msg):
		return
		yield

	def resides(self, p):
		return p in self and all(p not in s for s in self.__subs)

	def location(self, p):
		for s in self.__subs:
			if p in s:
				return s.location(p)
		return p in self

	def resting(self, name):
		if self.resides(name):
			return self.restarea
		else:
			for s in self.__subs:
				v = s.resting(name)
				if v is not None:
					return v
			return None

		


		
