from dataclasses import dataclass
import ShrimpSouls.actions as actions
import ShrimpSouls as ss
import ShrimpSouls.utils as utils
import random


@dataclass
class BaseNPC(ss.Entity):
	_acc: int = 8
	_eva: int = 9
	_att: int = 4
	_dfn: int = 4


	@classmethod
	def generate(cls, n, s):
		return tuple(cls(name=f"{cls.__name__}[{i}]") for i in range(s, s+n))

	def labeled(self, l):
		print(l)
		print(self.name)
		c1 = l.lower() == self.name.lower()

		if not c1:
			(n1, v1) = self.name.split('[')
			(n2, v2) = l.split('[')

			return n1.strip() == n2.strip() and int(v1[:-1]) == int(v2[:-1])

		return c1



@dataclass
class Goblin(BaseNPC):
	xp:  int = 1
	hp:  int = 10
	max_hp: int = 10
	_acc: int = 8
	_eva: int = 9
	_att: int = 4
	_dfn: int = 4

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	def __hash__(self):
		return hash(self.name)


@dataclass
class Wolf(BaseNPC):
	name: str = "Wolf"
	xp:  int = 3
	hp:  int = 25
	max_hp: int = 25
	_acc: int = 12
	_eva: int = 14
	_att: int = 9
	_dfn: int = 7

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	def __hash__(self):
		return hash(self.name)

@dataclass
class GoblinPriest(BaseNPC):
	name: str = "GoblinPriest"
	xp:  int = 5
	hp:  int = 20
	max_hp: int = 20
	_acc: int = 20
	_eva: int = 17
	_att: int = 10
	_dfn: int = 12

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(party)
		return [actions.HealTarget(attacker=actor, defender=target, dmg=random.randint(1, 4))]

	def __hash__(self):
		return hash(self.name)

@dataclass
class GoblinBrute(BaseNPC):
	name: str = "GoblinBrute"
	xp:  int = 7
	hp:  int = 30
	max_hp: int = 30
	_acc: int = 22
	_eva: int = 15
	_att: int = 33
	_dfn: int = 24

	def duel_action(self, actor, party, opponents):
		target = self.find_valid_target(opponents)
		return [actions.DamageTarget(attacker=actor, defender=target)]

	def __hash__(self):
		return hash(self.name)
