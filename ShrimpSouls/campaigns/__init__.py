import os
import enum
import atexit
import ShrimpSouls as ss
import persistent
from dataclasses import dataclass
import persistent.list as listing
import persistent.mapping as mapping
import ShrimpSouls.messages as messages

class BaseCampaign(persistent.Persistent):
	def __init__(self):
		self.__players = mapping.PersistentMapping()

	def is_joined(self, p):
		return p.name in self.__players

	def join(self, player):
		if self.is_joined(player):
			return messages.Message(
				msg=[f"{player.name} has already joined the campaign."])
		else:
			player.revive()
			player.reset_status()
			
			self.__players[player.name] = player

			return message.Message(
				msg=[f"{player.name} has joined the campaign"],
				users=[player])

	def step(self):
		return (self, messages.Message())

	@property
	def players(self):
		return utils.FrozenDict(self.__players)
	
	@property
	def npcs(self):
		return {}


	def enter(self, previous):
		pass

	def exit(self):
		pass


	def find_valid_target(self, att, dfn, evn, pos, amt=1):
		return []

	def get_npc(self, name):
		if isinstance(name, str):
			if name in self.npcs:
				return self.npcs[name]
			else:
				return None
		else:
			return name

	def get_player(self, name):
		if isinstance(name, str):
			if name in self.players:
				return self.players[name]
			else:
				return None
		else:
			if name.is_player:
				return name
			else:
				return None


class SubCampaign(persistent.Persistent):
	def __init__(self, parent):
		self.__parent = parent

	def is_joined(self, p):
		return self.__parent.is_joined(p)

	def join(self, player):
		self.__parent.is_joined(player)
		

	def step(self):
		return (self, messages.Message())

	@property
	def players(self):
		return self.__parent.players
	
	@property
	def npcs(self):
		return self.__parent.npcs


	def enter(self, previous):
		pass

	def exit(self):
		pass


	def find_valid_target(self, att, dfn, evn, pos, amt=1):
		return []

	@property
	def parent(self):
		return self.__parent


	def get_npc(self, name):
		if isinstance(name, str):
			if name in self.npcs:
				return self.npcs[name]
			else:
				return None
		else:
			return name

	def get_player(self, name):
		if isinstance(name, str):
			if name in self.players:
				return self.players[name]
			else:
				return None
		else:
			if name.is_player:
				return name
			else:
				return None
	