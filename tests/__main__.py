import ShrimpSouls as ss
import ShrimpSouls.actions as actions
import ShrimpSouls.npcs as npcs
import ShrimpSouls.utils as utils

class TestPlayer(ss.Player):
	def get_xp_req(self):
		return 0

class TestEnv:
	def __init__(self):
		self.p = TestPlayer(name="TestPlayer")

NPCS = [
	npcs.Goblin,
	npcs.Wolf,
	npcs.GoblinBrute,
	npcs.GoblinPriest,
	npcs.OrcWarrior,
	npcs.Ogre,
	npcs.Troll,
	npcs.Wraith,
	npcs.OxTitan,
	npcs.BloodGolem,
]

p = TestPlayer(name="TestPlayer")
for _ in p.update_class("juggernaut"): pass
att = ss.Attributes(
	vigor=0,
	endurance=0,
	strength=25,
	dexterity=0,
	intelligence=0,
	faith=0,
	luck=0,
	perception=0
)

for w in p.level_up_many(att.json):
	for m in w.msg:
		print(m)

print()
print()
for n in NPCS:
	e = n.make(0)
	print("-"*20 + n.__name__ + "-"*20)	

	print(f"{p.name}[max_hp] = {p.max_hp}")
	print(f"{e.name}[max_hp] = {e.max_hp}")
	print(f"Probability of hitting {n.__name__} is {utils.compute_prob(p, e)}")
	print(f"Damage against {n.__name__} is {utils.compute_dmg(p, e)}")
	print(f"Probability of being hit by {n.__name__} is {utils.compute_prob(e, p)}")
	print(f"Damage from {n.__name__} is {utils.compute_dmg(e, p)}")
	print()