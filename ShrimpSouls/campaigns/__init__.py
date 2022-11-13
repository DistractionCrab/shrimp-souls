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
	def __init__(self, name):
		self.__name = name
		self.__players = mapping.PersistentMapping()
		self.__npcs = mapping.PersistentMapping()

	def location(self, p):
		if p.name in self.__players:
			return self
		else:
			return None

	@property
	def name(self):
		return self.__name
	

	def __contains__(self, p):
		if isinstance(p, str):
			return p in self.__players

		return p.name in self.__players

	def step(self):
		return
		yield

	def action(self, src, msg):
		return
		yield

	def add_player(self, p):
		if p.name not in self.__players:
			self.__players[p.name] = p

	def add_npc(self, p):
		if p.name not in self.__npcs:
			self.__npcs[p.name] = p

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

	@property
	def actions(self):
		return tuple()

	def use_ability(self, p, abi, targets):
		yield messages.Respond(msg=[f"Cannot use abilities in {type(self)}"])

	@property
	def restarea(self):
		return True

class RootCampaign(BaseCampaign):
	def __init__(self, name):
		super().__init__(name)
		self.__subs = mapping.PersistentMapping()

	def __setitem__(self, index, value):
		self.__subs[index] = value

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

	def action(self, src, msg):
		if self.resides(src):
			yield from self._action(msg)
		else:
			for s in self.__subs.values():
				if src in s:
					yield from s.action(src, msg)

		

	def _action(self, msg):
		return
		yield

	def resides(self, p):
		return p in self and all(p not in s for s in self.__subs)

	def location(self, p):
		for s in self.__subs:
			if p in s:
				return s.location(p)
		return p in self

		


		
