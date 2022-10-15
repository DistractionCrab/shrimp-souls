import ShrimpSouls as ss
import random
import math
import enum
import ShrimpSouls.actions as actions
import ShrimpSouls.utils as utils

SOULMASS_THRESHOLD = 10

class ClassSpec:
	def compute_hit(self, a, d):
		return utils.compute_hit(a,d)


	def compute_dmg(self, a, d):
		return utils.compute_dmg(a, d)


	def score_eva(self, p):
		return p.level + 10

	def score_acc(self, p):
		return p.level + 10

	def score_att(self, p):
		return 1

	def score_dfn(self, p):
		return 1

	def basic_action(self, u, env):
		print("Milquetoast has no class action.")

	def targeted_action(self, u, target, env):
		print("Milquetoast has no class action.")


	def duel_action(self, actor, party, opponents):
		return [actions.DoNothing(player=actor)]

	def find_valid_target(self, op):
		op = list(filter(lambda x: x.invis == 0 and not x.dead, op))
		return random.choices(op)[0]

	def soulmass_count(self, p):
		return math.ceil(p.attributes.intelligence/SOULMASS_THRESHOLD)

	@property
	def cl_string(self):
		return "Milquetoast"


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
