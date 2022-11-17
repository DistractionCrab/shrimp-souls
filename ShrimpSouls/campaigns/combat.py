import random
import os
import persistent
import persistent.list
import persistent.mapping as mapping
from functools import reduce
from ShrimpSouls import npcs

import ShrimpSouls.utils as utils


import os
import atexit
import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps


class Combat(cps.BaseCampaign):
	def __init__(self, name):
		super().__init__(name)
		self.__queued = mapping.PersistentMapping()


	@property
	def restarea(self):
		return False

	def _add_player(self, player):
		pass	


	def step(self):
		if self.finished:
			yield messages.Message(
				msg=["Combat has already ended..."],
				recv=tuple(p for p in self.players),
				campinfo=self.campinfo())
		else:
			yield self.__do_combat()
			for p in self.players.values():
				yield messages.CharInfo(info=p, recv=[p.name])

	def _campinfo(self):
		if self.finished:
			return {
				"party": [],
				"npcs": [],
				"clearNPCs": True,
			}
		else:
			return {
				"party": [v.json for v in self.players.values()],
				"npcs": [v.json for v in self.npcs.values()],
				"clearNPCs": self.finished,
			}

	def start(self):
		return messages.Message(
			msg=["Combat has begun...  "],
			campinfo=self.campinfo())


	def __do_combat(self):
		party = list(self.players.values())
		enemies = list(self.npcs.values())

		order = list(a for a in (party + enemies) if not a.dead)
		random.shuffle(order)

		total = []

		for p in order:
			if self.finished:
				break
			if p.stun == 0 and not p.dead:
				actions = []
				if p.name in self.__queued:
					(abi, targets) = self.__queued[p.name]
					targets = targets if p.charm == 0 else tuple()
					actions = p.use_ability(abi, targets, self)
				else:
					if p.invis == 0:
						actions = p.random_action(self)
				for a in actions:
					a.apply()
					total.append(a.msg + " " + self.handle_dead_foes(a.receivers_npc))

		for p in order:
			if not p.dead:
				p.tick()

		if self.finished:
			if all(p.dead for p in self.players.values()):
				total.append({"type": "stepend", "msg": "The party has been defeated..."})
			if all(p.dead for p in self.npcs.values()):
				total.append(
					{"type": "stepend", "msg": "The party is Victorious!!!"})
		else:
			total.append({"type": "stepend", "msg": "The battle continues to rage..."})

		return messages.Message(
			msg=total, 
			campinfo=self.campinfo(),
			recv=tuple(self.players))

	

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


	def find_valid_target(self, att, ally, aliveq, amt=1, targets=tuple(), **kwds):
		if att.charm == 0:
			targets = (self.get_target(n) for n in targets)
			targets = tuple(p for p in targets if not p.dead)
		else:
			targets = tuple()

		if len(targets) >= amt:
			return tuple(random.sample(targets, k=amt))
		else:
			amt = amt - len(targets)
			pool = self.allies(att) if ally else self.opponents(att)
			pool = pool if not aliveq else filter(lambda x: not x.dead, pool)
			pool = tuple(p for p in pool if p.invis == 0 or random.random() < 0.1)
			pool = tuple(set(random.sample(pool, k=min(amt, len(pool)))))

			return pool + targets

	def use_ability(self, p, abi, targets):
		self.__queued[p.name] = (abi, targets)
		yield messages.Message(
			msg=[f"You have readied {abi} for the next turn."],
			recv=(p.name,))

