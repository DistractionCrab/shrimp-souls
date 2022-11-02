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

@dataclass
class BaseNPC(ss.Entity):
	commitfn: object = do_nothing
	_acc: int = 1
	_eva: int = 1
	_att: int = 1
	_dfn: int = 1
	_weaknesses: frozenset = field(default_factory=frozenset)
	_resists: frozenset = field(default_factory=frozenset)
	_tags: frozenset = field(default_factory=frozenset)

	def weak(self, v):
		return v in self._weaknesses

	def resist(self, v):
		return v in self._resists

	def has_tag(self, t):
		return t in self._tags

	@property
	def position(self):
		return ss.Positions.FRONT	
	

	def commit(self):
		self.commitfn(self)

	@classmethod
	def generate(cls, n, s, commitfn=do_nothing, prob=1.0):
		return tuple(
			cls(name=f"{cls.__name__}[{i}]",commitfn=commitfn)
			for i in range(s, s+n) if random.random() < prob)

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

	def random_action(self, u, env):
		return []

	def duel_action(self, env):
		target = env.find_valid_target(self, False, [ss.Positions.FRONT], True)
		if target is None:
			return [actions.DoNothing(player=self)]
		return [actions.DamageTarget(attacker=self, defender=target)]

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
	hp:  int = 100
	max_hp: int = 100
	_acc: int = 40
	_eva: int = 35
	_att: int = 45
	_dfn: int = 40

	def __hash__(self):
		return hash(self.name)


	


@dataclass
class Wolf(BaseNPC):
	xp:  int = 3
	hp:  int = 300
	max_hp: int = 300
	_acc: int = 50
	_eva: int = 45
	_att: int = 35
	_dfn: int = 50

	def __hash__(self):
		return hash(self.name)


@dataclass
class GoblinPriest(BaseNPC):
	xp:  int = 5
	hp:  int = 400
	max_hp: int = 400
	_acc: int = 150
	_eva: int = 210
	_att: int = 100
	_dfn: int = 180

	def __hash__(self):
		return hash(self.name)

	@property
	def position(self):
		return ss.Positions.BACK

	def duel_action(self, env):
		target = env.find_valid_target(self, True, ss.Positions, True, amt=3)
		return [
			actions.HealTarget(attacker=self, defender=t, dmg=random.randint(1, 6)) 
			for t in target]



@dataclass
class GoblinBrute(BaseNPC):
	xp:  int = 7
	hp:  int = 600
	max_hp: int = 600
	_acc: int = 180
	_eva: int = 190
	_att: int = 190
	_dfn: int = 200

	def __hash__(self):
		return hash(self.name)


@dataclass
class OrcWarrior(BaseNPC):
	xp:  int = 7
	hp:  int = 1200
	max_hp: int = 1200
	_acc: int = 310
	_eva: int = 300
	_att: int = 380
	_dfn: int = 300

	def __hash__(self):
		return hash(self.name)


@dataclass
class Ogre(BaseNPC):
	xp:  int = 15
	hp:  int = 2500
	max_hp: int = 2500
	_acc: int = 600
	_eva: int = 300
	_att: int = 600
	_dfn: int = 450

	def __hash__(self):
		return hash(self.name)

	def duel_action(self, env):
		target = env.find_valid_target(self, False, [ss.Positions.FRONT], True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		elif len(target) == 1:
			return [actions.DamageTarget(attacker=self, defender=target[0])]
		else:
			return [
				actions.DamageTarget(attacker=self, defender=target[0]),
				actions.DamageTarget(attacker=self, defender=target[1])]


@dataclass
class Troll(BaseNPC):
	xp:  int = 30
	hp:  int = 400
	max_hp: int = 400
	_acc: int = 32
	_eva: int = 29
	_att: int = 86
	_dfn: int = 70
	_weaknesses: frozenset = frozenset([actions.DamageType.Fire])

	def __hash__(self):
		return hash(self.name)

	def duel_action(self, env):
		target = env.find_valid_target(self, False, [ss.Positions.FRONT], True, amt=2)
		if len(target) == 0:
			return [actions.DoNothing(player=self)]
		elif len(target) == 1:
			return [actions.DamageTarget(attacker=self, defender=target[0])]
		else:
			return [
				actions.DamageTarget(attacker=self, defender=target[0]),
				actions.DamageTarget(attacker=self, defender=target[1]),
				actions.HealTarget(attacker=self, defender=self, dmg=20)]