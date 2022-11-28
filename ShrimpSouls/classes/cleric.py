import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

@dataclass
class Blessing(cs.Ability):
	t_amt: int = 3
	allyq: bool = True
	def act(self, u, t, env):		
		return [Action1(attacker=u, defender=r) for r in t]

@dataclass
class Cleanse(cs.Ability):
	allyq: bool = True
	def act(self, u, t, env):		
		return [Target1(attacker=u, defender=t)]

@dataclass
class HolyGavel(cs.Ability):
	t_amt: int = 3

	def act(self, u, targets, env):
		return [
			actions.DamageTarget(
				attacker=u,
				defender=t,
				statuses={ss.StatusEnum.evadown: lambda: 3},
				score_dmg=utils.ScoreDamage(scale=0.3))
			for t in targets
		]

ABI_MAP = {
	"autoattack": cs.autoattack,
	"blessing": Blessing(),
	"cleanse": Cleanse(),
	"holygavel": HolyGavel(),
}

class Cleric(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
		
	def max_hp(self, p):
		return cs.stat_map(p, mult=5, base=100, level=10, vigor=5)

	def score_acc(self, p):
		return cs.stat_map(p, level=10, faith=1, perception=1)

	def score_eva(self, p):
		return cs.stat_map(p, level=10, dexterity=1)

	def score_att(self, p):
		return cs.stat_map(p, level=10, faith=1, strength=1)

	def score_dfn(self, p):
		return cs.stat_map(p, level=10, faith=1, strength=1)

	@property
	def cl_string(self):
		return "Cleric"


@dataclass
class Action1(actions.Action):
	def apply(self):
		ss.StatusEnum.defup.stack(self.defender, amt=3)
		self.msg += f"{self.attacker.name} prayer bolster's {self.defender.name}'s defense. "


@dataclass
class Target1(actions.Action):
	def apply(self):
		ss.StatusEnum.burn.use(self.defender, self.defender.status.burn)
		ss.StatusEnum.attdown.use(self.defender,self.defender.status.attdown)
		ss.StatusEnum.evadown.use(self.defender,self.defender.status.evadown)
		ss.StatusEnum.accdown.use(self.defender,self.defender.status.accdown)
		ss.StatusEnum.defdown.use(self.defender,self.defender.status.defdown)
		ss.StatusEnum.poison.use(self.defender,self.defender.status.poison)
		ss.StatusEnum.stun.use(self.defender,self.defender.status.stun)

		self.msg += f"{self.attacker.name} has cleansed {self.defender.name} of their debuffs."