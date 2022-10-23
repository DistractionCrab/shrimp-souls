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
	_acc: int = 8
	_eva: int = 9
	_att: int = 4
	_dfn: int = 4
	#weaknesses: list = field(default_factory=list)
	#resists: list = field(default_factory=list)
	#tags: list = field(default_factory=list)

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



@dataclass
class Goblin(BaseNPC):
	xp:  int = 1
	hp:  int = 10
	max_hp: int = 10
	_acc: int = 8
	_eva: int = 9
	_att: int = 4
	_dfn: int = 4

	def __hash__(self):
		return hash(self.name)


	


@dataclass
class Wolf(BaseNPC):
	xp:  int = 3
	hp:  int = 25
	max_hp: int = 25
	_acc: int = 12
	_eva: int = 14
	_att: int = 9
	_dfn: int = 7

	def __hash__(self):
		return hash(self.name)


@dataclass
class GoblinPriest(BaseNPC):
	xp:  int = 5
	hp:  int = 20
	max_hp: int = 20
	_acc: int = 20
	_eva: int = 17
	_att: int = 10
	_dfn: int = 12

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
	hp:  int = 30
	max_hp: int = 30
	_acc: int = 22
	_eva: int = 15
	_att: int = 28
	_dfn: int = 24

	def __hash__(self):
		return hash(self.name)


@dataclass
class OrcWarrior(BaseNPC):
	xp:  int = 7
	hp:  int = 72
	max_hp: int = 72
	_acc: int = 26
	_eva: int = 24
	_att: int = 50
	_dfn: int = 48

	def __hash__(self):
		return hash(self.name)


@dataclass
class Ogre(BaseNPC):
	xp:  int = 15
	hp:  int = 160
	max_hp: int = 160
	_acc: int = 26
	_eva: int = 21
	_att: int = 54
	_dfn: int = 50

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

