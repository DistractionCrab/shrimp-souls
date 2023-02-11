import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns.combat as combat
import ShrimpSouls.campaigns.dungeons as dng
import ShrimpSouls.npcs as npcs


class CombatRoom(dng.EmptyRoom):
	def __init__(self):
		super().__init__()
		self.__combat = None
		self.__finished = False
		self.__treasures = []

	@property
	def completed(self):
		return self.__finished
	
	@property
	def json(self):
		if self.completed:
			return super().json
		else:
			return {
				"rtype": "combat"
			}

	@property
	def room_icon(self):
		return 'C'

	def step(self, camp):
		if self.__finished:
			yield from super().step(camp)
		else:
			if self.__combat is not None:
				if self.__combat.finished:
					self.__finished = True
				else:
					yield from self.__combat.step()

	def enter(self, camp):
		if not self.__finished:
			if self.__combat is None:
				self.__combat = DungeonCombat()
				for p in camp.players.values():
					yield from self.__combat.add_player(p)

				yield camp.broadcast(msg=["Combat has begun..."])

	def campinfo(self, camp):
		if self.__combat is None or self.__finished:
			return super().campinfo(camp)
		else:
			return self.__combat.campinfo()

	def exit(self, camp):
		return
		yield

	def use_ability(self, p, abi, targets, camp):
		yield from self.__combat.use_ability(p, abi, targets)

	def use_item(self, p, index, targets, camp):
		yield from self.__combat.use_item(p, index, targets)

	def add_player(self, p):
		yield from self.__combat.add_player(p)


class DungeonCombat(combat.Combat):
	def __init__(self):
		super().__init__("arena")

	def _add_player(self, p):
		p.revive()
		p.reset_status()
		added = npcs.get_enemy(p.level, len(self.npcs))

		for n in added:
			self.add_npc(n)

		yield messages.Message(
			msg=[f"{p.name} has joined the battle, and so do {', '.join(n.name for n in added)}"],
			recv=tuple(p for p in self.players))