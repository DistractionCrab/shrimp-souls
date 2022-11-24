import ShrimpSouls as ss
import random
import math
import enum
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils
from dataclasses import dataclass

SOULMASS_THRESHOLD = 10

@dataclass
class Ability:
	t_amt: int = 1
	allyq: bool = False
	aliveq: bool = True

	def __call__(self, u, targets, env):
		if self.t_amt == 0:
			return self.act(u, u, env)
		else:
			targets = env.find_valid_target(
				u,
				self.allyq, 
				self.aliveq, 
				targets=targets, 
				amt=self.t_amt)

			if len(targets) == 0:
				return tuple()
			else:
				if self.t_amt == 1:
					return self.act(u, targets[0], env)
				else:
					return self.act(u, targets, env)

	def act(self, u, targets, env):
		return tuple()



def score_wrap(p, **kwds):
	return lambda p: stat_map(p, **kwds)

def acc_wrap(p, **kwds):
	return lambda p: utils.acc_scale(p, stat_map(p, **kwds))

def att_wrap(p, **kwds):
	return lambda p: utils.att_scale(p, stat_map(p, **kwds))

def eva_wrap(p, **kwds):
	return lambda p: utils.eva_scale(p, stat_map(p, **kwds))

def def_wrap(p, **kwds):
	return lambda p: utils.def_scale(p, stat_map(p, **kwds))

def stat_map(
	p,
	base=0,
	mult=1,
	level=0,
	vigor=0,
	endurance=0,
	strength=0,
	dexterity=0,
	intelligence=0,
	faith=0,
	luck=0,
	perception=0):
	
	return math.ceil(
		mult*(
			base 
			+ level * p.level
			+ p.attributes.vigor * vigor
			+ p.attributes.endurance * endurance
			+ p.attributes.strength * strength
			+ p.attributes.dexterity * dexterity
			+ p.attributes.intelligence * intelligence
			+ p.attributes.faith * faith
			+ p.attributes.luck * luck
			+ p.attributes.perception * perception))

def autoattack(actor, targets, env):
	return [
		actions.DamageTarget(attacker=actor, defender=t) 
		for t in env.find_valid_target(actor, False, True, targets=targets)]

ABI_MAP = {
	"autoattack": autoattack
}

class ClassSpec:
	def max_hp(self, p):
		return stat_map(p, base=50, level=20)

	@property
	def abi_map(self):
		return ABI_MAP

	@property
	def ability_list(self):
		return tuple(self.abi_map.keys())

	def score_eva(self, p):
		return stat_map(p, level=9)

	def score_acc(self, p):
		return stat_map(p, level=9)

	def score_att(self, p):
		return stat_map(p, level=9)

	def score_dfn(self, p):
		return stat_map(p, level=9)

	def score_will(self, p):
		return stat_map(p, level=9)

	def score_char(self, p):
		return stat_map(p, level=9)

	def score_fort(self, p):
		return stat_map(p, level=9)

	def score_vit(self, p):
		return stat_map(p, level=9)


	def duel_action(self, actor, env):
		return [actions.DoNothing(player=actor)]

	def soulmass_count(self, p):
		return math.ceil(p.attributes.intelligence/SOULMASS_THRESHOLD)

	def random_action(self, u, env):
		m = self.abi_map
		if len(m) > 0:
			a = random.sample(list(m.values()),k=1)[0]
			return a(u, tuple(), env)
		else:
			return []

	@property
	def cl_string(self):
		return "Milquetoast"


	def use_ability(self, u, abi, targets, env):
		if len(self.abi_map) == 0:
			return [actions.Error(info="Milquetoast has no abilities to use.")]
		elif abi in self.abi_map:
			return self.abi_map[abi](u, targets, env)
		else:
			return [actions.Error(info=f"No such ability: {abi}")]

import ShrimpSouls.classes.knight as knight
import ShrimpSouls.classes.juggernaut as juggernaut
import ShrimpSouls.classes.warrior as warrior
import ShrimpSouls.classes.swordsman as swordsman
import ShrimpSouls.classes.fencer as fencer
import ShrimpSouls.classes.sorcerer as sorcerer
import ShrimpSouls.classes.spellblade as spellblade
import ShrimpSouls.classes.pyromancer as pyromancer
import ShrimpSouls.classes.cryomancer as cryomancer
import ShrimpSouls.classes.priest as priest
import ShrimpSouls.classes.cleric as cleric
import ShrimpSouls.classes.paladin as paladin
import ShrimpSouls.classes.thief as thief
import ShrimpSouls.classes.assassin as assassin
import ShrimpSouls.classes.bard as bard

class Classes(enum.Enum):
	Milquetoast = ClassSpec()
	Knight = knight.Knight()
	Juggernaut = juggernaut.Juggernaut()
	Warrior = warrior.Warrior()
	Swordsman = swordsman.Swordsman() 
	Fencer = fencer.Fencer()
	Sorcerer = sorcerer.Sorcerer()
	Spellblade = spellblade.SpellBlade()
	Pyromancer = pyromancer.Pyromancer()
	Cryomancer = cryomancer.Cryomancer()
	Priest = priest.Priest()
	Cleric = cleric.Cleric()
	Paladin = paladin.Paladin()
	Thief = thief.Thief() 
	Assassin = assassin.Assassin()
	Bard = bard.Bard()

	def score_att(self, u):
		return self.value.score_att(u)

	def score_dfn(self, u):
		return self.value.score_dfn(u)

	def score_acc(self, u):
		return self.value.score_acc(u)

	def score_eva(self, u):
		return self.value.score_eva(u)
