import enum
import random
import math
import itertools as itools
import persistent
import persistent.list as plist
import persistent.mapping as mapping

import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps
import ShrimpSouls.utils as utils
import ShrimpSouls.campaigns.combat as combat
import ShrimpSouls.npcs as npcs
import ShrimpSouls.items as items

from collections import deque

class EnvironmentTag:
	Cold = enum.auto()
	Hot = enum.auto()
	Lava = enum.auto()
	Poison = enum.auto()
	Miasmic = enum.auto()
	Fog = enum.auto()

MIN_MAP_WIDTH = 10

class Dungeon(cps.BaseCampaign):
	def __init__(self):
		super().__init__("Dungeon")
		self.__map = None
		self.__polled_actions = {}



	def resting(self, name):
		return self.__map.restarea

	def campinfo(self):
		if self.__combat is None:
			return {
				"name": "dungeon",
				"party": list(p.json for p in self.players.values()),
			}
		else:
			return self.__combat.campinfo()


	def step(self):
		if self.__map is None:
			self.__map = DungeonMap(len(self.players))
			yield self.broadcast(msg=["The dungeon is being prepared, please wait with the mimics."])
		else:
			if self.__map.complete:
				self.__map = None
				yield self.broadcast(msg=['The dungeon has been completed already.'])
			else:
				pass

	def action(self, src, msg):
		if msg["action"] == "leave":
			yield messages.Response(
				msg=("You will leave the arena when combat has finished.",),
				recv=(src,))



	def _add_player(self, p):
		if self.__combat is not None:
			self.__combat.add_player(p)
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

	def use_item(self, p, index, targets):
		if self.__combat is None:
			yield messages.Message(
				msg=(f"Cannot use items in while waiting on the arena...",),
				recv=(p.name,))
		else:
			yield from self.__combat.use_item(p, index, targets)

	def action(self, src, msg):
		match msg:
			case {"type": "vote", "field": f, "choice": c}: 
				yield from self.__register_vote(src, f, c)

	def __register_vote(self, player, field, choice):
		cur = self.__polled_actions.setdefault(field, {})
		cur.setdefault(player, choice)
		yield messages.Response(
			msg=[f"You have voted to {choice} for {field}."]
			recv=(player,))


class EmptyRoom:
	def __init__(self):
		self.visited = False
		self.completed = False

ROOM_SET = list({
	EmptyRoom,
})

def get_random_room():
	return random.choice(ROOM_SET)

class DungeonMap(persistent.Persistent):
	class Edge(persistent.Persistent):
		def __init__(self, dest, locked=False):
			self.__dest = dest
			self.locked = locked

		@property
		def dest(self):
			return self.__dest
		

	def __init__(self, pcount):
		self.__pcount = pcount
		self.__map = {}
		self.__rooms = {}
		self.__loc = self.__generate()

	@property
	def location(self):
		return self.__loc
	

	def __generate(self):
		# Proportion of tiles to use
		prop = random.uniform(0.2, 0.4)
		width = math.ceil(max(MIN_MAP_WIDTH, math.log(self.__pcount, 2)))
		start = (random.randint(0, width-1), random.randint(0, width-1))
		max_rooms = math.ceil(prop*width**2)
		self.__width = width

		self.__rooms[start] = get_random_room()

		available = deque()

		loc = start
		
		while len(self.__rooms) < max_rooms:
			c = self.__get_random_direction(loc)

			if c is not None:
				r = get_random_room()
				self.__rooms[c] = r
				self.__map.setdefault(loc, []).append(DungeonMap.Edge(c))
				self.__map.setdefault(c, []).append(DungeonMap.Edge(loc))


			loc = random.choices(
				self.rooms, 
				weights=[1/len(self.__map[r])**3 for r in self.__rooms.keys()])[0]

		
		return start

	def __get_random_direction(self, loc):
		(x, y) = loc
		choices = [
			(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)
		]
		#choices = filter(lambda p: p not in self.__rooms,choices)
		choices = filter(
			lambda p: all(a >= 0 and a < self.__width for a in p), 
			choices)
		choices = list(choices)
		if len(choices) == 0:
			return None
		else:
			return random.choices(
				list(choices),
				weights=[1/len(self.__map[r])**3 if r in self.__map else 1 for r in choices])[0]

	def __leads(self, r1, c1, r2, c2):
		if (r1, c1) in self.__rooms and (r2, c2) in self.__rooms:
			for e in self.__map[(r1, c1)]:
				if e.dest == (r2, c2):
					return True
		
		return False

	def ascii_map(self):
		print(f'rooms = {len(self.__rooms)}')
		print(f"Rooms made: {list(self.__rooms.keys())}")
		def resolve(row, col):
			r = row // 2
			c = col // 2
			if row % 2 == 0:
				if col % 2 == 0:
					return "+"
				else:
					return "-"
			else:
				if col % 2 == 0:
					return "|"
				else:					
					return "0" if (r, c) in self.__rooms else " "

		icons = [
			[resolve(r, c) for r in range(2*self.__width+1)]
			for c in range(2*self.__width+1)
		]

		for row in range(1, 2*self.__width):
			for col in range(1 + row % 2, 2*self.__width, 2):
				if row % 2 == 1:
					r = row // 2
					c = col // 2 - 1

					c1 = self.__leads(r, c, r, c + 1)
					if c1:
						icons[col][row] = "-"
					else:
						icons[col][row] = " "
				else:
					r = row // 2 - 1
					c = col // 2
					c1 = self.__leads(r, c, r+1, c)
					if c1:
						icons[col][row] = "|"
					else:
						icons[col][row] = " "
					
				

		for r in range(2*self.__width+1):
			for c in range(2*self.__width+1):
				print(icons[c][r], end="")
			print()


	@property
	def rooms(self):
		return tuple(self.__rooms.keys())

class GenParams:
	# Probability of placing a key.
	KEY_PLACE = 0.05

class KeyItems(enum.Enum):
	Key = enum.auto()