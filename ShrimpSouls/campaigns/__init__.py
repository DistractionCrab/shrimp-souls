import os
import enum
import atexit
import ShrimpSouls as ss
import persistent
from dataclasses import dataclass

class NullCampaign(persistent.Persistent):
	def join(self, player):
		pass

	def step(self):
		return (self, ["No campaign active to step."])

	@property
	def players(self):
		return tuple()
	
	@property
	def npcs(self):
		return tuple()


	def enter(self, previous):
		pass

	def exit(self):
		pass

	def close(self):
		pass

	def find_valid_target(self, att, dfn, evn, pos, amt=1):
		return None