import ShrimpSouls as ss
import ShrimpSouls.classes as cs
from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
import random
import math

def hamstring(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def slice(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"hamstring": hamstring,
	"slice": slice,
}

class Swordsman(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=4, vigor=4)
		return 20 + 4*p.level + 4*p.attributes.vigor

	def score_acc(self, p):
		return cs.stat_map(p, base=10, level=0.5, dexterity=0.5)
		return 10 + math.ceil(p.level/2) + math.ceil(p.attributes.dexterity/2)

	def score_eva(self, p):
		return cs.stat_map(p, base=10, level=0.35, dexterity=0.65)
		return 10 + math.ceil(p.level*0.35) + math.ceil(p.attributes.dexterity*0.65)

	def score_att(self, p):
		return cs.stat_map(p, strength=2.5, dexterity=3.5)
		return math.ceil(2.5*p.attributes.strength + 3.5*p.attributes.dexterity)

	def score_dfn(self, p):
		return cs.stat_map(p, level=2, strength=1, dexterity=1)
		return 2*p.level + p.attributes.strength + p.attributes.dexterity

	def basic_action(self, u, env):
		npcs = list(env.npcs)
		targets = random.sample(npcs, k=min(3, len(npcs)))

		return [Action1(attacker=u, defender=t) for t in targets]

		#print(f"{u.name} hamstrings some of their foes, decreasing their evasion.")

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

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

	@property
	def cl_string(self):
		return "Swordsman"

@dataclass
class Action1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_evadown(amt=2)
			self.msg += f"{self.attacker.name} has hamstrung {self.defender.name}. "
		else:
			self.msg += f"{self.attacker.name} has missed their hamstring. "

@dataclass
class Target1(actions.Action):
	def apply(self):
		if utils.compute_hit(self.attacker, self.defender)[0]:
			self.defender.stack_bleed(amt=random.randint(1, 2))
			self.msg += f"{self.attacker.name}'s sharp blades slice into {self.defender.name}. "
		else:
			self.msg += f"{self.attacker.name}'s blades miss {self.defender.name}. "
