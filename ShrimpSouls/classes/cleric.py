import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import random
import math

def blessing(u, targets, env):
	targets = env.find_valid_target(u, True, ss.Positions, True, amt=3)

	return [Action1(attacker=u, defender=t) for t in targets]

def cleanse(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for cleanseing.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"blessing": blessing,
	"cleanse": cleanse,
}

class Cleric(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
		
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=5, vigor=6)

	def score_acc(self, p):
		return cs.stat_map(p, base=11, level=1)

	def score_eva(self, p):
		return cs.stat_map(p, base=9, level=1)

	def score_att(self, p):
		return cs.stat_map(p, strength=3, faith=3)

	def score_dfn(self, p):
		return cs.stat_map(p, strength=2, faith=3)

	def basic_action(self, u, env):
		players = list(p for p in env.players if not p.dead)
		targets = random.sample(players, k=min(3, len(players)))

		return [Action1(attacker=u, defender=t) for t in targets]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]
		

	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, [ss.Positions.FRONT], True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Cleric"


@dataclass
class Action1(actions.Action):
	def apply(self):
		self.defender.stack_defup(amt=3)
		self.msg += f"{self.attacker.name} prayer bolster's {self.defender.name}'s defense. "


@dataclass
class Target1(actions.Action):
	def apply(self):
		self.defender.use_burn(self.defender.burn)
		self.defender.use_attdown(self.defender.attdown)
		self.defender.use_evadown(self.defender.evadown)
		self.defender.use_accdown(self.defender.accdown)
		self.defender.use_defdown(self.defender.defdown)
		self.defender.use_poison(self.defender.poison)
		self.defender.use_stun(self.defender.stun)

		self.msg += f"{self.attacker.name} has cleansed {self.defender.name} of their debuffs."