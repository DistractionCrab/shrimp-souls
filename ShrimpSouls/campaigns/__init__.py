import os
import enum
import diskcache as dc
import ShrimpSouls as ss

CACHE_DIR = ss.CACHE_DIR/"campaigns"
PLAYER_CACHE = dc.Cache(CACHE_DIR)

if 'players' not in PLAYER_CACHE:
	PLAYER_CACHE['players'] = []

class NullCampaign:
	def step(self):
		print("No campaign active to step.")

	@property
	def start_msg(self):
		return "NullCampaign has started, there is nothing to do now...  Sadge"


	def get_player(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_enemy(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")

	def get_target(self, name):
		raise ValueError(f"No such target as {name} in a NullCampaign")
			


import ShrimpSouls.campaigns.arena as arena
class Campaigns(enum.Enum):
	Null = NullCampaign()
	Arena = arena.Arena()