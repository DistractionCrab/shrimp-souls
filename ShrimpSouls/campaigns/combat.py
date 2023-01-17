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
				yield messages.CharInfo(info=p)

	def campinfo(self):
		if self.finished:
			return {
				"name": self.name,
				"party": [],
				"npcs": [],
				"clearNPCs": True,
			}
		else:
			return {
				"name": self.name,
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
			if p.status.stun == 0 and not p.dead:
				for a in p.tick():
					total.append(a)
					
				actions = []
				if p.name in self.__queued:					
					actions = self.__queued[p.name].act(p, self)
				else:
					if p.status.invis == 0:
						actions = p.random_action(self)

				for a in actions:
					a.apply()
					total.append(a.msg + " " + self.handle_dead_foes(a.receivers_npc))
			elif p.status.stun > 0 and not p.dead:
				for a in p.tick():
					total.append(a)

		self.__queued.clear()

		

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

	def use_ability(self, p, abi, targets):
		self.__queued[p.name] = UseAbility(abi, targets)
		yield messages.Response(
			msg=[f"You have readied {abi} for the next turn aimed at {', '.join(targets)}"],
			recv=(p.name,))

	def use_item(self, p, index, targets):
		if index < len(p.inventory):
			self.__queued[p.name] = UseItem(p.inventory[index], targets)

			yield messages.Response(
				msg=[f"You have readied {p.inventory[index].display} for the next turn aimed at {', '.join(targets)}"],
				recv=(p.name,))
		else:
			yield messages.Response(
				msg=[f"You do not have an item in the {index} slot."],
				recv=(p.name,))


class UseAbility:
	def __init__(self, abi, targets):
		self.__targets = targets
		self.__abi = abi

	def act(self, p, env):
		if p.status.charm == 0:
			return p.use_ability(self.__abi, self.__targets, env)
		else:
			return p.random_action(env)

		

class UseItem:
	def __init__(self, item, targets):
		self.__targets = targets
		self.__item = item

	def act(self, p, env):
		if p.status.charm == 0:
			return self.__item.act(p, self.__targets, env)
		else:
			return p.random_action(env)



