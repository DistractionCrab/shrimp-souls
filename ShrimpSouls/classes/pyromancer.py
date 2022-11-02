from ShrimpSouls.classes import ClassSpec
from dataclasses import dataclass
import ShrimpSouls as ss
import ShrimpSouls.classes as cs
import ShrimpSouls.utils as utils
import ShrimpSouls.actions as actions
import random
import math

def pyroclasm(u, targets, env):
	targets = env.find_valid_target(u, False, ss.Positions, True, amt=3)
		
	if targets is None:
		return []
	else:
		return [Action1(attacker=u, defender=t) for t in targets]

def fireball(u, targets, env):
	if len(targets) == 0:
		return [actions.Error(info=f"No targets specified for poaching.")]
	t = env.get_target(targets[0])
	return [Target1(attacker=u, defender=t)]

ABI_MAP = {
	"pyroclasm": pyroclasm,
	"fireball": fireball,
}

class Pyromancer(ClassSpec):
	@property
	def abi_map(self):
		return ABI_MAP
	
	@property
	def ability_list(self):
		return tuple(ABI_MAP.keys())
	
	def max_hp(self, p):
		return cs.stat_map(p, base=20, level=2, vigor=4)
		return 20 + 2*p.level + 4 * p.attributes.vigor

	@property
	def position(self):
		return ss.Positions.BACK

	def score_acc(self, p):
		return cs.stat_map(p, base=13, intelligence=1, faith=1, dexterity=0.25)

	def score_eva(self, p):
		return cs.stat_map(p, base=12, level=1.25)

	def score_att(self, p):
		return cs.stat_map(p, faith=3, intelligence=3)

	def score_dfn(self, p):
		return cs.stat_map(p, base=3, level=1.5)

	def basic_action(self, u, env):
		npcs = list(n for n in env.npcs if not n.dead)
		targets = random.sample(npcs, k=min(3, len(npcs)))
		return [Action1(attacker=u,defender=t) for t in targets]
			

	def targeted_action(self, u, target, env):
		return [Target1(attacker=u, defender=target)]

	def use_ability(self, u, abi, targets, env):
		if abi in ABI_MAP:
			return ABI_MAP[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]


	def ultimate_action(self, u, players, npcs):
		pass

	def duel_action(self, actor, env):
		if actor.invis == 0:
			target = env.find_valid_target(actor, False, list(ss.Positions), True)
			return [actions.DamageTarget(attacker=actor, defender=target)]
		else:
			return []

	@property
	def cl_string(self):
		return "Pyromancer"

@dataclass
class Action1(actions.EffectAction):
	def on_hit(self):
		t = random.randint(1, 3)
		self.defender.stack_burn(amt=t)
		self.msg += f"{self.attacker.name} has burned {self.defender.name} for {t} turns."

	def on_miss(self):
		self.msg += f"{self.attacker.name} failed to burn {self.defender.name}."


@dataclass
class Target1(actions.DamageTarget):
	score_dmg: tuple = utils.score_dmg(m1=1.3)
	statuses: tuple = ((ss.StatusEnum.burn, 2),)