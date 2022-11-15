import random
import persistent
import persistent.mapping as mapping

import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps
import ShrimpSouls.utils as utils



class Hub(cps.RootCampaign):
	def __init__(self):
		super().__init__("Shrimplink Shrine")
		self["arena"] = arena.Arena()

	@property
	def areaname(self):
		return "Shrimplink Hub"


	def _action(self, src, msg):
		match msg:
			case {"arena": True, **objs}: print(f"{src.name} has gone to the arena.")
			case _: print(f"Unrecognized action: {msg}")


