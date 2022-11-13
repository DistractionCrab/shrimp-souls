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
import ShrimpSouls.campaigns as cps


class Combat(cps.BaseCampaign):
	def __init__(self):
		super().__init__()
		self.__queued = mapping.PersistentMapping()
		self._generate(self.players)
	
	def _generate(self, newplayers):
		pass

	@property
	def restarea(self):
		return False

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


	def step(self):
		if len(self.players) == 0:
			yield  messages.Message(msg=["No players available, exiting combat..."])
		else if len(self.npcs) == 0:
			yield  messages.Message(msg=["No enemies available, exiting combat..."])
		else:
			yield self.__do_combat()


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
				if p.name in self.__queued:
					(abi, targets) = self.__queued[p.name]
					targets = targets if p.charm == 0 else tuple()
					actions = p.use_ability(abi, targets, self)
				else:
					if p.invis == 0:
						actions = p.random_action(p, self)
					
				for a in actions:
					a.apply()
					total.append(a.msg + " " + self.handle_dead_foes(a.receivers_npc))
					rec_p.update(a.receivers)
					rec_n.update(a.receivers_npc)

		for p in order:
			if not p.dead:
				p.tick()

		if self.finished:
			if all(p.dead for p in self.players.values()):
				total.append("The party has been defeated...")
			if all(p.dead for p in self.npcs.values()):
				total.append("The party is Victorious!!!")
		else:
			total.append("The battle continues to rage.")


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
		self.__queued[p.name] = (abi, targets)
		yield messages.Respons(msg=[f"You have readied {abi} for the next turn."])

