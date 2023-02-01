import enum
import random
import math
import sys
import time
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

	@property
	def map(self):
		return self.__map

	def resting(self, name):
		return self.__map is None	

	def campinfo(self):
		if self.__map is None:
			return {}
		else:
			return self.__map.campinfo(self)

	def resting(self, name):
		return self.__map is None

	def step(self):
		if self.__map is None:
			self.__map = DungeonMap(len(self.players))
			yield self.broadcast(
				msg=["The dungeon is being prepared, please wait with the mimics."],
				campinfo=self.campinfo())
		else:
			if self.__map.complete:
				self.__map = None
				yield self.broadcast(
					msg=['The dungeon has been completed already.'],
					campinfo=self.campinfo())
			else:
				yield from self.__map.step(self)
				if all(p.hp <= 0 for p in self.players.values()):
					yield self.broadcast(
						msg=[{"type": "stepend", "msg": "All players are dead, exiting the dungeon."}],
						campinfo=self.campinfo())
					self.__map = None
					for p in self.players.values():
						p.revive()
						p.reset_status()
				elif self.__map.complete:
					yield self.broadcast(
						msg=[{"type": "stepend", "msg": "The dungeon has been completed!."}],
						campinfo=self.campinfo())
					self.__map = None
					for p in self.players.values():
						p.revive()
						p.reset_status()
				else:
					yield self.broadcast(campinfo=self.campinfo())


	def find_valid_target(self, att, ally, alive, **kwds):
		if self.__combat is None:
			return tuple()
		else:
			return self.__combat.find_valid_target(att, ally, alive, **kwds)

	def use_ability(self, p, abi, targets):
		self.__map.use_ability(p, abi, targets, self)

	def use_item(self, p, index, targets):
		self.__map.use_item(p, index, targets, self)

	def action(self, src, msg):
		yield from self.__map.action(src, msg, self)

	def _add_player(self, p):
		yield self.broadcast(msg=[f"{p.name} has joined the dungeon!!!"])


class EmptyRoom:
	def __init__(self):
		self.__visited = False
		self.__polls = mapping.PersistentMapping()

	@property
	def completed(self):
		return self.__visited

	@property
	def json(self):
		return {
			"rtype": "empty"
		}

	@property
	def visited(self):
		return self.__visited
	
	def visit(self):
		self.__visited = True
	
	def enter(self, camp):
		self.visit()
		return
		yield

	def exit(self, camp):
		return 
		yield

	def step(self, camp):
		if len(self.__polls) > 0:
			info = self.campinfo(camp)["move_poll"]
			d = max(info, key=lambda x: info[x])
			yield from camp.map.move(Directions[d], camp)
			self.__polls.clear()
		else:
			yield camp.broadcast(
				msg=[{"type": "stepend", "msg": "No votes have been cast, no action will be taken."}])

	def campinfo(self, camp):
		sum_n = 0
		sum_s = 0
		sum_e = 0
		sum_w = 0

		for v in self.__polls.values():
			if v == Directions.North:
				sum_n += 1
			elif v == Directions.South:
				sum_s += 1
			elif v == Directions.East:
				sum_e += 1
			elif v == Directions.West:
				sum_w += 1

		return {
			"move_poll": {
				Directions.North.name: sum_n,
				Directions.South.name: sum_s,
				Directions.East.name: sum_e,
				Directions.West.name: sum_w,
			}
		}


	@property
	def room_icon(self):
		return '0'
	


	def action(self, src, msg, camp):
		if "vote" in msg:
			try:
				d = Directions[msg['vote']]
				self.__polls[src] = d
				yield messages.Response(
					msg=[f"You have voted to travel {d.name}"],
					recv=(src.name,))
			except:
				yield messages.Response(
					msg=[f"Invalid option to vote for: {msg['vote']}"],
					recv=(src,))

	def use_ability(self, p, abi, targets, camp):
		p = camp[p]
		if p.acted:
			yield messages.Response(
				msg=["You have already acted this turn."],
				src=(p.name,))
			
		else:
			msgs = []
			for a in p.use_ability(abi, targets, camp):
				msgs.append(a.apply())
			yield camp.broadcast(msg=msgs)
			p.did_act()

	def use_item(self, p, index, targets, camp):
		if index < len(p.inventory):
			i = p.inventory[index]
			msgs = []
			for a in i.act(p, targets, camp):
				msgs.append(a.apply())

			yield camp.broadcast(msg=msgs)

		else:
			yield messages.Response(
				msg=[f"You do not have an item in the {index} slot."],
				recv=(p.name,))


def get_random_room():
	return random.choice(ROOM_SET)()

class Directions(enum.Enum):
	North = (0, -1)
	South = (0, 1)
	East = (1, 0)
	West = (-1, 0)

def compute_dir(start, end):
	x1, y1 = start
	x2, y2 = end

	if x2 - x1 == 0 and y2 - y1 == 1:
		return Directions.North
	elif x2 - x1 == 0 and y2 - y1 == -1:
		return Directions.South
	elif x2 - x1 == 1 and y2 - y1 == 0:
		return Directions.East
	elif x2 - x1 == 0 and y2 - y1 == 1:
		return Directions.West

class Edge(persistent.Persistent):
	def __init__(self, dest, locked=False):
		self.__dest = dest
		self.locked = locked

	@property
	def dest(self):
		return self.__dest

class DungeonMap(persistent.Persistent):
	def __init__(self, pcount):
		self.__pcount = pcount
		self.__map = {}
		self.__rooms = {}
		self.__loc = self.__generate()
		self.__uid = int(time.time())

	@property
	def complete(self):
		return all(r.completed for r in self.__rooms.values())
	

	@property
	def moveable(self):
		edges = self.__map[self.__loc].keys()
		return [
			compute_dir(self.__loc, e) for e in edges
		]
	

	@property
	def complete(self):
		return all(r.completed for r in self.__rooms.values())
	
	@property
	def location(self):
		return self.__rooms[self.__loc]

	@property
	def rooms(self):
		return tuple(self.__rooms.keys())

	
	

	def __generate(self):
		# Proportion of tiles to use
		prop = random.uniform(0.2, 0.4)
		width = math.ceil(max(MIN_MAP_WIDTH, math.log(self.__pcount+1, 2)))
		start = (random.randint(0, width-1), random.randint(0, width-1))
		max_rooms = math.ceil(prop*width**2)
		self.__width = width

		self.__rooms[start] = EmptyRoom()

		available = deque()

		loc = start
		
		while len(self.__rooms) < max_rooms:
			c = self.__get_random_direction(loc)

			if c is not None:
				r = get_random_room()
				self.__rooms[c] = r
				self.__map.setdefault(loc, []).append(Edge(c))
				self.__map.setdefault(c, []).append(Edge(loc))


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
					return self.__rooms[(r, c)].room_icon if (r, c) in self.__rooms else " "

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

	def step(self, camp):
		yield from self.location.step(camp)

	def __map_info(self):
		indices = [l for l in self.__rooms.keys()]
		return {
			"room_index": indices,
			"rooms": {
				i: self.__rooms[r].json for (i, r) in enumerate(self.__rooms)
			},
			"paths": {
				i: [e.dest for e in self.__map[l]]
				for (i, l) in enumerate(self.__rooms)
			},
			'location': self.__loc,
			'uid': self.__uid,
			'width': self.__width,
		}


	def campinfo(self, camp):
		r = self.__rooms[self.__loc]
		i = {
			"inventory": [],
			"map": self.__map_info(),
			"party": [p.json for p in camp.players.values()]
		}
		return i | r.campinfo(camp)

	def action(self, src, msg, camp):
		yield from self.location.action(src, msg, camp)

	def adjacent(self, p1, p2):
		for a in self.__map[p1]:
			if p2 == a.dest:
				return True

		return False

	def move(self, dir, camp):
		# Get the new location.
		new_loc = tuple(sum(x) for x in zip(self.__loc, dir.value))

		if new_loc in self.__rooms and self.adjacent(self.__loc, new_loc):
			old_room = self.location
			yield from old_room.exit(camp)
			self.__loc = new_loc
			yield from self.location.enter(camp)

			yield camp.broadcast(msg=[{"type": "stepend", "msg":f"You are now in room {self.__loc}"}])

	def use_ability(self, p, abi, targets, camp):
		yield from self.location.use_ability(p, abi, targets, camp)

	def use_item(self, p, index, targets, camp):
		yield from self.location.use_item(p, index, targets, camp)


	

# Simple local class used to control how dungeons are generated. This will change
# as search through good parameters.
class GenParams:
	# Probability of placing a key.
	KEY_PLACE = 0.05

class KeyItems(enum.Enum):
	Key = enum.auto()

import ShrimpSouls.campaigns.dungeons.combat as cmb
ROOM_SET = list({
	EmptyRoom,
	cmb.CombatRoom
})

class RoomAction:
	def step(self, camp):
		pass