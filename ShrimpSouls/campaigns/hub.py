import random
import persistent
import persistent.mapping as mapping

import ShrimpSouls as ss
import ShrimpSouls.messages as messages
import ShrimpSouls.campaigns as cps
import ShrimpSouls.utils as utils



class Hub(cps.BaseCampaign):
	def __init__(self):
		super().__init__("Shrimplink Shrine")
		self.__stashes = mapping.PersistentMapping()


