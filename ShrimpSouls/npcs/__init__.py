from dataclasses import dataclass, field
import enum
import ShrimpSouls.actions as actions
import ShrimpSouls as ss
import ShrimpSouls.utils as utils
import random

def do_nothing(self):
	pass

class NPCTags(enum.Enum):
	Undead = enum.auto()

	def tagged(self, p):
		return p.has_tag(self)



@dataclass
class BaseNPC(ss.Entity):
	commitfn: object = do_nothing
	_acc: int = 1
	_eva: int = 1
	_att: int = 1
	_dfn: int = 1
	_will: int = 1
	_vit: int = 1
	_char: int = 1
	_fort: int = 1
	_weaknesses: frozenset = field(default_factory=frozenset)
	_resists: frozenset = field(default_factory=frozenset)
	_tags: frozenset = field(default_factory=frozenset)
	_immunities: frozenset = field(default_factory=frozenset)
	bossq: bool = False
	lvrange: range = range(1, 1000000)

	def weak(self, v):
		return v in self._weaknesses

	def immune(self, d):
		return d in self._immunities

	def resist(self, v):
		return v in self._resists

	def has_tag(self, t):
		return t in self._tags	

	def commit(self):
		self.commitfn(self)

	@classmethod
	def generate(cls, n, s, commitfn=do_nothing, prob=1.0):
		return tuple(
			cls(name=f"{cls.__name__}[{i}]",commitfn=commitfn)
			for i in range(s, s+n) if random.random() < prob)

	@classmethod
	def make(cls, i):
		return cls(name=f"{cls.__name__}[{i}]")

	def labeled(self, l):
		try:
			c1 = l.lower() == self.name.lower()

			if not c1:
				(n1, v1) = self.name.split('[')
				(n2, v2) = l.split('[')

				return n1.strip() == n2.strip() and int(v1[:-1]) == int(v2[:-1])

			return c1
		except:
			return False


	def random_action(self, env):
		target = env.find_valid_target(self, False, True)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		return [actions.DamageTarget(attacker=self, defender=target[0])]

	def use_ability(self, abi, targets, env):
		return self.random_action(env)

	def __hash__(self):
		return hash(self.name)

	@property
	def json(self):
		return {
				'name': self.name,
				'hp': self.hp,
				'max_hp': self.max_hp,
				'xp': self.xp,
				'status': self.status.__dict__
			}



@dataclass
class Goblin(BaseNPC):
	xp:  int = 1
	hp:  int = 200
	max_hp: int = 200
	_acc: int = 10
	_eva: int = 10
	_att: int = 10
	_dfn: int = 10
	lvrange: range = range(1, 4)

	def __hash__(self):
		return hash(self.name)


@dataclass
class Wolf(BaseNPC):
	xp:  int = 3
	hp:  int = 350
	max_hp: int = 350
	_acc: int = 35
	_eva: int = 20
	_att: int = 35
	_dfn: int = 10
	lvrange: range = range(2, 4)

	def __hash__(self):
		return hash(self.name)

@dataclass
class SkeletonArcher(BaseNPC):
	xp:  int = 5
	hp:  int = 245
	max_hp: int = 245
	_acc: int = 50
	_eva: int = 25
	_att: int = 40
	_dfn: int = 30
	lvrange: range = range(3, 7)
	_weaknesses: frozenset = frozenset([
		actions.DamageType.Holy, 
		actions.DamageType.Strike])
	_tags: frozenset = frozenset([NPCTags.Undead])

	def __hash__(self):
		return hash(self.name)

@dataclass
class GoblinPriest(BaseNPC):
	xp:  int = 5
	hp:  int = 300
	max_hp: int = 300
	_acc: int = 70
	_eva: int = 80
	_att: int = 45
	_dfn: int = 50
	lvrange: range = range(5, 10)

	def __hash__(self):
		return hash(self.name)


	def random_action(self, env):
		target = env.find_valid_target(self, True, True, amt=3)
		return [
			actions.HealTarget(attacker=self, defender=t, dmg=random.randint(1, 6)) 
			for t in target]



@dataclass
class GoblinBrute(BaseNPC):
	xp:  int = 7
	hp:  int = 450
	max_hp: int = 450
	_acc: int = 75
	_eva: int = 70
	_att: int = 90
	_dfn: int = 70
	lvrange: range = range(5, 10)
	

	def __hash__(self):
		return hash(self.name)


@dataclass
class StoneGolem(BaseNPC):
	xp:  int = 10
	hp:  int = 450
	max_hp: int = 450
	_acc: int = 90
	_eva: int = 60
	_att: int = 100
	_dfn: int = 110
	lvrange: range = range(7, 12)
	_resists: frozenset = frozenset([
		actions.DamageType.Magic,
		actions.DamageType.Pierce,
		actions.DamageType.Slash,
		actions.DamageType.Fire,
		actions.DamageType.Lightning,])
	_weaknesses: frozenset = frozenset([
		actions.DamageType.Magic, 
		actions.DamageType.Strike])
	_tags: frozenset = frozenset([NPCTags.Undead])

	def __hash__(self):
		return hash(self.name)


@dataclass
class OrcWarrior(BaseNPC):
	xp:  int = 11
	hp:  int = 1000
	max_hp: int = 1000
	_acc: int = 120
	_eva: int = 110
	_att: int = 140
	_dfn: int = 135
	lvrange: range = range(10, 15)

	def __hash__(self):
		return hash(self.name)


@dataclass
class Ogre(BaseNPC):
	xp:  int = 15
	hp:  int = 2500
	max_hp: int = 2500
	_acc: int = 160
	_eva: int = 100
	_att: int = 170
	_dfn: int = 145
	lvrange: range = range(10, 15)

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		elif len(target) == 1:
			return [actions.DamageTarget(attacker=self, defender=target[0])]
		else:
			return [
				actions.DamageTarget(attacker=self, defender=target[0]),
				actions.DamageTarget(attacker=self, defender=target[1])]


@dataclass
class Cockatrice(BaseNPC):
	xp:  int = 12
	hp:  int = 700
	max_hp: int = 700
	_acc: int = 110
	_eva: int = 110
	_att: int = 140
	_dfn: int = 135
	lvrange: range = range(13, 17)

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		else:
			return [actions.DamageTarget(
				attacker=self, 
				defender=target[0],
				statuses={ss.StatusEnum.stun: lambda: random.randint(0, 1)})]

@dataclass
class Troll(BaseNPC):
	xp:  int = 30
	hp:  int = 4000
	max_hp: int = 4000
	_acc: int = 180
	_eva: int = 160
	_att: int = 220
	_dfn: int = 170
	_weaknesses: frozenset = frozenset([actions.DamageType.Fire])
	lvrange: range = range(15, 20)

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		elif len(target) == 1:
			return [actions.DamageTarget(attacker=self, defender=target[0])]
		else:
			return [
				actions.DamageTarget(attacker=self, defender=target[0]),
				actions.DamageTarget(attacker=self, defender=target[1]),
				actions.HealTarget(attacker=self, defender=self)]




@dataclass
class Wraith(BaseNPC):
	xp:  int = 30
	hp:  int = 2500
	max_hp: int = 2500
	_acc: int = 180
	_eva: int = 210
	_att: int = 150
	_dfn: int = 160
	_weaknesses: frozenset = frozenset([actions.DamageType.Fire])
	_resists: frozenset = frozenset([
		actions.DamageType.Magic,
		actions.DamageType.Strike,
		actions.DamageType.Slash,])
	_tags: frozenset = frozenset([NPCTags.Undead])
	lvrange: range = range(15, 20)

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		else:
			return [actions.DamageTarget(
				attacker=self, 
				defender=target[0],
				statuses={ss.StatusEnum.poison: lambda: 2, ss.StatusEnum.bleed: lambda: 3})]


@dataclass
class OxTitan(BaseNPC):
	xp:  int = 100
	hp:  int = 110000
	max_hp: int = 110000
	_acc: int = 250
	_eva: int = 210
	_att: int = 320
	_dfn: int = 220
	_weaknesses: frozenset = frozenset([actions.DamageType.Pierce,])
	_immunities: frozenset = frozenset([
			ss.StatusEnum.charm,
		])
	bossq: bool = True
	lvrange: range = range(20, 26)

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		elif len(target) == 1:
			return [actions.DamageTarget(attacker=self, defender=target[0])]
		else:
			return [
				actions.DamageTarget(attacker=self, defender=target[0]),
				actions.DamageTarget(attacker=self, defender=target[1])]

@dataclass
class BloodGolem(BaseNPC):
	xp:  int = 40
	hp:  int = 10000
	max_hp: int = 10000
	_acc: int = 250
	_eva: int = 190
	_att: int = 190
	_dfn: int = 310
	lvrange: range = range(20, 26)
	_weaknesses: frozenset = frozenset([
		actions.DamageType.Pierce,
		actions.DamageType.Strike,
		actions.DamageType.Slash,
		actions.DamageType.Magic,
		actions.DamageType.Dark,
		actions.DamageType.Nature,])

	_immunities: frozenset = frozenset([
			ss.StatusEnum.charm,
			ss.StatusEnum.bleed,
			ss.StatusEnum.poison,
			ss.StatusEnum.defdown,
		])

	def __hash__(self):
		return hash(self.name)

	def random_action(self, env):
		target = env.find_valid_target(self, False, True)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		else:
			return [actions.DamageTarget(
				attacker=self, 
				defender=target[0],
				abilityrange=actions.AbilityRange.Medium,
				statuses={
					ss.StatusEnum.poison: lambda: 2, 
					ss.StatusEnum.bleed: lambda: 2,
					ss.StatusEnum.defdown: lambda: 2,
					ss.StatusEnum.attdown: lambda: 2,
				})]

def __check(a):
	return isinstance(a, type) and issubclass(a, BaseNPC) and a != BaseNPC and not a.bossq

import sys
NPCS = list(a for a in sys.modules[__name__].__dict__.values() if __check(a))
NPCS = {
	r: [n for n in NPCS if n.lvrange == r]
	for r in (n.lvrange for n in NPCS)
}


def get_enemy(level, sindex, amt=1):
	valid = tuple(r for r in NPCS.keys() if level in r)

	choice = random.choices(valid, k=1)[0]
	return [c.make(sindex + i) for (i, c) in enumerate(random.choices(NPCS[choice], k=amt))]
