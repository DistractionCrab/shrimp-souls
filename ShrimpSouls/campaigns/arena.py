import random
import os
from functools import reduce
from ShrimpSouls import npcs
from ShrimpSouls.campaigns import NullCampaign


class Arena(NullCampaign):
	def __init__(self, players):
		super().__init__(players)
		# Two dictionaries for positions. p1 is the party, p2 is the npcs.
		self.__statedata = ({}, {})
		

	def restore_encounter(self, npcs, statedata, finished):

		super().restore_encounter(npcs, statedata, finished)

		self.__statedata = eval(statedata)


	def step(self):
		if len(self.players) == 0:
			print("No players available for the arena: type !join to join the campaign!")
		elif self.finished:
			print("The arena has begun!")
			self.__setup_arena()			
		else:
			self.__do_combat()

	def __find_appropriate_encounter(self):
		avg = int(sum(p.level for p in self.players)/len(self.players))
		print(f"avg = {avg}")
		try:
			k = next(k for k in ENCOUNTERS.keys() if avg in k)
			(l, m) = random.choices(ENCOUNTERS[k])[0]
			return l(len(self.players)), m
		except StopIteration:
			print("banana")
			(l, m) = (
				lambda n: [npcs.Goblin(npcid=i) for i in range(3*n)],
				"Many Goblins"
			)

			return l(len(self.players)), m

	def __setup_arena(self):
		self.npcs, m = self.__find_appropriate_encounter()
		
		for p in self.players:
			p.revive()
			p.reset_status()
		print(f"Today's foes in the arena are {m}.")

	def __do_combat(self):
		order = list(self.players) + list(self.npcs)
		order = list(filter(lambda x: not x.dead and x.stun <= 0, order))
		random.shuffle(order)


		p_fetch = lambda x: self.players if x in self.players else self.npcs
		o_fetch = lambda x: self.npcs if x in self.players else self.players
		#actions =  [p.duel_action(p, p_fetch(p), o_fetch(p)) for p in order if not p.stun > 0]
		#actions =  [self.get_action(p) for p in order if  p.stun <= 0]
		#actions = reduce(lambda a, b: a + b, actions, [])
		for p in order:
			p.tick()

		alivep = [p for p in self.players if not p.dead]
		aliven = [p for p in self.npcs if not p.dead]

		for p in order:
			if self.finished:
				break
			actions = self.get_action(p)
			for a in actions:
				a.apply()
				#print(a.msg)
				if self.finished:
					break


		msg = ""

		dead = [p for p in alivep if p.dead]

		if len(dead) > 0 and len(dead) <= 3:
			msg += f"{', '.join(p.name for p in dead)} have perished in the arena. "
		elif len(dead) > 0:
			msg += "Many players have perished in the arena. "

		dead1 = [p for p in aliven if p.dead]

		if len(dead1) > 0:
			if len(dead1) <= 3:
				msg += f"{', '.join(p.name + f'[{p.npcid}]' for p in dead1)} have perished in the arena. "
			else:
				msg += "Many foes have perished in the arena. "

			xp = sum(p.xp for p in dead1)
			for p in self.players:
				p.add_shrimp(xp)

			msg += f"The party gains {xp} shrimp. "
			

		if len(dead) == 0 and len(dead1) == 0:
			msg += "No deaths so far."

		if not self.finished:
			msg += f"The battle, however, continues to rage..."
		else:
			if all(p.dead for p in self.players):
				msg += "The match has ended. The party has been defeated..."
			elif all(p.dead for p in self.npcs):
				msg += f"The match has ended. The party is victorious!!!"


		# Handle ticking for buffs/debuffs.
		order = list(self.players) + list(self.npcs)
		order = list(filter(lambda x: not x.dead, order))

		for p in order:
			p.tick()

		print(msg)

		
	def get_action(self, entity):
		#print(entity.label)
		tt = entity.get_taunt_target()
		if entity.is_player:
			if tt is not None:
				return entity.duel_action(entity, self.players, [self.get_labeled(tt)])
			elif entity.charm > 0:
				return entity.duel_action(entity, self.npcs, self.players)			
			else:
				return entity.duel_action(entity, self.players, self.npcs)
		elif entity.is_npc:
			if tt is not None:
				return entity.duel_action(entity, self.npcs, [self.get_labeled(tt)])
			elif entity.charm > 0:
				return entity.duel_action(entity, self.players, self.npcs)
			else:
				return entity.duel_action(entity, self.npcs, self.players)
		else:
			return [actions.DoNothing(player=entity)]


	def statedata(self):
		return self.__statedata

	@property
	def finished(self):
		return all(p.dead for p in self.players) or all(p.dead for p in self.npcs)

	def update_interface(self):
		with open(os.path.join(os.path.split(__file__)[0], "interfacedata.js"), 'w') as out:
			players = [[p.name, p.health, p.max_health] for p in self.players]
			enemies = [[p.name + f"[{p.npcid}]", p.hp, p.max_hp] for p in self.npcs]
			random.shuffle(players)
			random.shuffle(enemies)
			out.write(JAVASCRIPT.format(players=players, enemies=enemies))
			out.flush()
		with open(os.path.join(os.path.split(__file__)[0], "interface.html"), 'w') as out:
			out.write(HTML)
			out.flush()

JAVASCRIPT = """
const PLAYERS = {players};
const ENEMIES = {enemies};
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Shrimp Souls Interface</title>
	<style type="text/css">
		body {
			color:  white;
			font-size: 200%;
			font-family: Arial;
			font-weight: 900;
			-webkit-text-stroke-width: 2px;
  			-webkit-text-stroke-color: black;
  			background-color: black;
  			text-overflow: ellipsis;
		}

		.hpbar {
			background-image: URL("../resources/healthbar.jpg");
			background-size: 100% 100%;
			background-repeat: no-repeat;
			width:  300px;
			height: 25px;
			border-style: solid;
			border-width: 6px;
			border-color: black;
			border-radius: 10px;
			opacity: 0%;
		}

		table {
			margin-left: auto;
			margin-right: auto;
		}

		#phpbarcontainer {
			background-color: rgba(255, 0, 0, 0);
			background-size:  90% 90%;
			border-radius: 10px;
		}

		#ehpbarcontainer {
			background-color: rgba(255, 0, 0, 0);
			background-size:  90% 90%;
			border-radius: 10px;
		}
	</style>
	<script type="text/javascript" src="interfacedata.js"></script>
	<script type="text/javascript">
		const R_INT = 128;
		const FADE_IN = 1000;
		const FADE_OUT = 1000;
		const STABLE = 10000;
		const HIDDEN = 1000;

		class Looper {
			constructor() {
				var pin = localStorage.getItem("pindex");
				var ein = localStorage.getItem("eindex");

				if (pin == null  ) {
					this.pindex = 0;
					this.eindex = 0;
				} else {
					if (pin >= PLAYERS.length || ein > ENEMIES.length) {
						this.pindex = 0;
						this.eindex = 0;
					} else {
						this.pindex = parseInt(pin);
						this.eindex = parseInt(ein);	
					}
					
				}
				
				this.php = document.getElementById("php");
				this.pname = document.getElementById("playername");
				this.pcont = document.getElementById("phpbarcontainer");
				this.ehp = document.getElementById("ehp");
				this.ename = document.getElementById("enemyname");
				this.econt = document.getElementById("ehpbarcontainer");

				this.phpval = document.getElementById("phpdisplay");
				this.ehpval = document.getElementById("ehpdisplay");

				this.fadeout = false;
				this.fadein = false;
				this.stable = false;
				this.hidden = true;

				this.timer = Date.now();

				this.set_invis()

				//var player = PLAYERS[Math.floor(Math.random() * PLAYERS.length)];
				//var enemy = ENEMIES[Math.floor(Math.random() * ENEMIES.length)];

				this.set_info(PLAYERS[this.pindex], ENEMIES[this.eindex]);

			}

			next_alive(l, index) {
				const d = l[index];
				var c = 0;
				while (c < l.length) {
					c += 1;
					index = (index + 1) % l.length;
					if (l[index][1] > 0) {
						return l[index]
					}
				}
				return d;
			}
			

			update_bars() {
				var dt = Date.now() - this.timer;
				//console.log(dt);
				if (this.stable) {
					this.set_full_vis()					
					if (dt > STABLE) {
						this.stable = false;
						this.fadeout = true;
						this.timer = Date.now();
					}
				} else if (this.fadeout) {
					if (dt > FADE_OUT) {
						this.fadeout = false;
						this.hidden = true;

						//var player = this.next_alive(PLAYERS,);
						//var enemy = this.next_alive(ENEMIES, (this.eindex + 1) % ENEMIES.length);

						localStorage.setItem("pindex", (this.pindex + 1) % PLAYERS.length);
						localStorage.setItem("eindex", (this.eindex + 1) % ENEMIES.length);

						location.reload();

					} else {
						var r = 1-dt/FADE_OUT;
						var p = Math.min(Math.ceil(r * 100), 100)
						
						this.set_vis(r, p);
					}
				} else if (this.fadein) {
					if (dt > FADE_IN) {
						this.fadein = false;
						this.stable = true;
						this.timer = Date.now();
						this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
						this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
					} else {
						var r = dt/FADE_IN;
						var p = Math.min(Math.ceil(r * 100), 100);

						this.set_vis(r, p);
					}
				} else if (this.hidden) {					
					if (dt > HIDDEN) {
						this.timer = Date.now();
						this.fadein = true;
						this.hidden = false;
					}
				}
			}

			set_full_vis() {
				this.php.style.opacity = `100%`;
				this.ehp.style.opacity = `100%`;
				this.pname.style.opacity = `100%`;
				this.ename.style.opacity = `100%`;
				this.phpval.style.opacity = '100%';
				this.ehpval.style.opacity = '100%';
				this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
				this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
			}

			set_vis(r, p) {
				this.php.style.opacity = `${p}%`;
				this.pname.style.opacity = `${p}%`;
				this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;

				this.ehp.style.opacity = `${p}%`;
				this.ename.style.opacity = `${p}%`;
				this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;

				this.phpval.style.opacity = `${p}%`;
				this.ehpval.style.opacity = `${p}%`;
			}

			set_invis() {
				this.php.style.opacity = `0%`;
				this.pname.style.opacity = `0%`;
				this.ename.style.opacity = `0%`;
				this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, 0)`;
				this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, 0)`;
				this.phpval.style.opacity = '0%';
				this.ehpval.style.opacity = '0%';
			}

			set_info(player, enemy) {
				var p = Math.max(0, Math.ceil(player[1]/player[2]*100));
				var ep = Math.max(0, Math.ceil(enemy[1]/enemy[2]*100));

				this.php.style.backgroundSize = `${p}% 100%`;
				this.ehp.style.backgroundSize = `${ep}% 100%`;
				this.pname.innerHTML = player[0];
				this.ename.innerHTML = enemy[0];

				this.phpval.innerHTML = `HP: [${player[1]}/${player[2]}]`;
				this.ehpval.innerHTML = `HP: [${enemy[1]}/${enemy[2]}]`;
			}
		}

		

		function main() {
			const LOOPER = new Looper();
			

			setInterval(function() {LOOPER.update_bars();}, 100)
		}

		document.addEventListener('DOMContentLoaded', main, false);
	</script>
</head>
<body>
	<table>
		<tr>
			<td>
				<table id=playerinfo>
					<tr>
						<td id="playername"></td>
					</tr>
					<tr>
						<td id=phpbarcontainer><div class="hpbar" id="php"></div></td>
					</tr>
					<tr >
						<td id=phpdisplay></td>
					</tr>
				</table>
			</td>
			<td>
				<table id=enemyinfo>
					<tr>
						<td id="enemyname"></td>
					</tr>
					<tr>
						<td id=ehpbarcontainer><div class="hpbar" id="ehp"></div></td>
					</tr>
					<tr >
						<td id=ehpdisplay></td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
</body>
</html>
"""

ENCOUNTERS = {
	range(1, 6): [
		(
			lambda n: [npcs.Goblin(npcid=i) for i in range(3*n)],
			"Many Goblins"
		),
		(
			lambda n: (
				[npcs.Goblin(npcid=i) for i in range(2*n)] +
				[npcs.Wolf(npcid=i) for i in range(n)]),
			"Many Goblins and some wolves"
		),
	]

}