import os
import enum
import atexit
import ShrimpSouls as ss


class NullCampaign:
	def join(self, player):
			raise ValueError(f"{p.name} cannot join a NullCampaign")

	def step(self):

		print("No campaign active to step.")
		return "No campaign active to step."

	@property
	def players(self):
		return tuple()
	
	@property
	def npcs(self):
		return tuple()

	@property
	def start_msg(self):
		return "NullCampaign has started, there is nothing to do now...  Sadge"


	def get_player(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_enemy(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_target(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def enter(self, previous):
		return ''

	def exit(self):
		return ''

	def close(self):
		pass

	def find_valid_target(self, att, dfn, evn, pos):
		return None
			


import ShrimpSouls.campaigns.arena as arena
class Campaigns(enum.Enum):
	Null = NullCampaign()
	Arena = arena.Arena()
	ArenaSetup = arena.Setup()

def close():
	for a in Campaigns:
		a.value.close()

atexit.register(close)