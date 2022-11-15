import random
import persistent
import persistent.mapping as mapping

import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps
import ShrimpSouls.utils as utils
import ShrimpSouls.campaigns.combat as combat

COMBAT_KEY = "**Arena Combat**"

class Arena(cps.RootCampaign):
	def __init__(self):
		super().__init__("Arena Lobbdy")
		self.__auto = mapping.PersistentMapping()
		self.__prep = True

	def __camp_info(self, p):
		return {
			"type": "Arena Lobby",
			"auto": self.__auto[p.name] if p.name in self.__auto else False
		}

	@property
	def areaname(self):
		return "Arena Lobby"

	@property
	def act_always(self):
		return True

	def _step(self):
		if len(self) == 0:
			if self.__prep:
				self.__prep = False
				yield self.broadcast(msg=("The arena will begin shortly...",))
			else:
				if len(self.players) > 0:
					for p in self.players.values():
						p.revive()
						p.reset_status()
					self[COMBAT_KEY] = Combat("The Arena", players=self.players)
					yield self[COMBAT_KEY].start()
		else:
			if self[COMBAT_KEY].finished:
				pass
			


	def _action(self, src, msg):
		match msg:
			case {"enter": True, **objs}: yield from self.__join(src)
			case {"auto": v, **objs}: yield from self.__auto(src, v)
			case {"leave": True, **objs}: yield from self.__leave(src)
			case _: yield messages.Response(msg=(f"Unknown message from {src.name}: {msg}",))

	def __auto(self, src, v):
		if v:
			self.__auto[src.name] = src
			yield messages.Response(
				msg=("You will now automatically join the arena whilst in the lobby.",),
				campinfo=self.__camp_info(src))

		else if src.name in self.__auto:
			del self.__auto[src.name]
			yield messages.Response(
				msg=("You will no longer automatically join the arena.",),
				campinfo=self.__camp_info(src))


	def __leave(self, p):
		if p in self:
			del self[p]
			yield self.broadcast(msg=(f"{p.name} has left the arena...",))

	def __join(self, p):		
		if p not in self:
			self.add_player(p)
			self.__auto[p.name] = True

			if len(self) > 0:
				yield self.broadcast(
					msg=(f"{p.name} has joined the arena lobby! One is already progress, please wait.",),
					campinfo=self.__camp_info(src))
			else:
				yield self.broadcast(
					msg=(f"{p.name} has joined the arena lobby!",),
					campinfo=self.__camp_info(src))
		else:
			yield self.broadcast(
				msg=(f"{p.name} is already in the lobby!!",),
				campinfo=self.__camp_info(src))


	def __setup_arena(self):
		self[COMBAT_KEY] = combat.Combat()
