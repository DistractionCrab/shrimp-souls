import random
import persistent
import persistent.list as plist
import persistent.mapping as mapping

import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps
import ShrimpSouls.utils as utils
import ShrimpSouls.campaigns.combat as combat
import ShrimpSouls.npcs as npcs

class Arena(cps.BaseCampaign):
	def __init__(self):
		super().__init__("arena")
		self.__combat = None	

	def resting(self, name):
		return self.__combat is None

	def _campinfo(self):
		if self.__combat is None:
			return {
				"party": list(p.json for p in self.players.values()),
			}
		else:
			return self.__combat._campinfo()


	def step(self):
		if self.__combat is None:
			self.__combat = ArenaCombat()
			for p in self.players.values():
				p.revive()
				p.reset_status()
				for _ in self.__combat.add_player(p):
					pass
			yield self.broadcast(
				msg=["The Arena will be starting soon!"],
				campinfo=self.campinfo())
		else:
			yield from self.__combat.step()

			if self.__combat.finished:
				self.__combat = None


	def _add_player(self, p):
		yield self.broadcast(msg=[f"{p.name} has joined the arena!!!"])


	def _add_npc(self, p):
		yield self.broadcast(msg=[f"{p.name} has joined the arena!!!"])


	def find_valid_target(self, att, ally, alive, **kwds):
		if self.__combat is None:
			return tuple()
		else:
			return self.__combat.find_valid_target(att, ally, alive, **kwds)

	def use_ability(self, p, abi, targets):
		if self.__combat is None:
			yield messages.Message(
				msg=(f"Cannot use abilities in while waiting on the arena...",),
				recv=(p.name,))
		else:
			yield from self.__combat.use_ability(p, abi, targets)


import ShrimpSouls.campaigns.combat as combat
class ArenaCombat(combat.Combat):
	def __init__(self):
		super().__init__("arena")

	def _add_player(self, p):
		p.revive()
		p.reset_status()
		added = []
		for (r, ns) in ENCOUNTERS.items():
			if p.level in r:
				c = ns[random.randint(0, len(ns)-1)]
				if c.bossq:
					if random.random() < 0.005:
						n = c.make(len(self.npcs))
						self.add_npc(n)
						added.append(n)
				else:
					n = c.make(len(self.npcs))
					self.add_npc(n)
					added.append(n)
						
		yield messages.Message(
			msg=[f"{p.name} has joined the battle, and so do {', '.join(n.name for n in added)}"],
			recv=tuple(p for p in self.players))





ENCOUNTERS = {
	range(1, 8): [npcs.Goblin, npcs.Wolf],
	range(5, 14): [npcs.GoblinBrute, npcs.GoblinPriest],
	range(10, 18): [npcs.Ogre, npcs.OrcWarrior],
	range(15, 23): [npcs.Troll, npcs.Wraith],
	range(20, 20000): [npcs.OxTitan, npcs.BloodGolem],

}
