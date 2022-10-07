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

	def __setup_arena(self):
		self.npcs = (npcs.Goblin(npcid=i) for i in range(3*len(self.players)))
		for p in self.players:
			p.revive()
			p.reset_status()
		print("Today's foes in the arena are many goblins.")

	def __do_combat(self):
		order = list(self.players) + list(self.npcs)
		order = filter(lambda x: not x.dead, order)
		random.shuffle(order)


		p_fetch = lambda x: self.players if x in self.players else self.npcs
		o_fetch = lambda x: self.npcs if x in self.players else self.players
		actions =  [p.duel_action(p, p_fetch(p), o_fetch(p)) for p in order if not p.stun > 0]
		actions = reduce(lambda a, b: a + b, actions, [])
		for p in order:
			p.tick()

		alivep = [p for p in self.players if not p.dead]
		aliven = [p for p in self.npcs if not p.dead]

		for a in actions:
			if self.finished:
				break
			else:
				a.apply()

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

			msg += f"The party gains {x} shrimp."
			

		if len(dead1)

		if len(dead) == 0 and len(dead1) == 0:
			msg += "No deaths so far."

		if not self.finished:
			msg += f"The battle, however, continues to rage..."
		else:
			if all(p.dead for p in self.players):
				msg += "The match has ended. The party has been defeated... No Experience will be awarded."
			elif all(p.dead for p in self.npcs):
				

				

				msg += f"The match has ended. The party is victorious! The party gains {xp} XP!"


		print(msg)

			

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
				this.index = 0;
				this.eindex = 0;
				this.php = document.getElementById("php");
				this.pname = document.getElementById("playername");
				this.pcont = document.getElementById("phpbarcontainer");
				this.ehp = document.getElementById("ehp");
				this.ename = document.getElementById("enemyname");
				this.econt = document.getElementById("ehpbarcontainer");
				this.fadeout = false;
				this.fadein = false;
				this.stable = false;
				this.hidden = true;

				this.timer = Date.now();

				this.php.style.opacity = `0%`;
				this.pname.style.opacity = `0%`;
				this.ename.style.opacity = `0%`;
				this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, 0)`;
				this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, 0)`;

				var player = PLAYERS[Math.floor(Math.random() * PLAYERS.length)];
				var enemy = ENEMIES[Math.floor(Math.random() * ENEMIES.length)];
				//var player = chance.weighted(PLAYERS);
				//var enemy = chance.weighted(ENEMIES);
				var p = Math.ceil(player[1]/player[2]*100);
				var ep = Math.ceil(enemy[1]/enemy[2]*100);

				this.php.style.backgroundSize = `${p}% 100%`;
				this.ehp.style.backgroundSize = `${ep}% 100%`;
				this.index = (this.index + 1) % PLAYERS.length;
				this.eindex = (this.eindex + 1) % ENEMIES.length;
				this.pname.innerHTML = player[0];
				this.ename.innerHTML = enemy[0];
			}

			update_bars() {
				var dt = Date.now() - this.timer;
				//console.log(dt);
				if (this.stable) {
					this.php.style.opacity = `100%`;
					this.ehp.style.opacity = `100%`;
					this.pname.style.opacity = `100%`;
					this.ename.style.opacity = `100%`;
					this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
					this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, 1)`;
					if (dt > STABLE) {
						this.stable = false;
						this.fadeout = true;
						this.timer = Date.now();
					}
				} else if (this.fadeout) {
					if (dt > FADE_OUT) {
						this.fadeout = false;
						this.hidden = true;

						location.reload()

					} else {
						var r = 1-dt/FADE_OUT;
						var p = Math.min(Math.ceil(r * 100), 100)
						this.php.style.opacity = `${p}%`;
						this.pname.style.opacity = `${p}%`;
						this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;

						this.ehp.style.opacity = `${p}%`;
						this.ename.style.opacity = `${p}%`;
						this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;
						
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

						this.php.style.opacity = `${p}%`;
						this.pname.style.opacity = `${p}%`;
						this.pcont.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;

						this.ehp.style.opacity = `${p}%`;
						this.ename.style.opacity = `${p}%`;
						this.econt.style.backgroundColor = `rgba(${R_INT}, 0, 0, ${r})`;
						//console.log(`rgba(255, 0, 0, ${r})`);
					}
				} else if (this.hidden) {
					
					if (dt > HIDDEN) {
						this.timer = Date.now();
						this.fadein = true;
						this.hidden = false;
					}
				}
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
				</table>
			</td>
		</tr>
	</table>
</body>
</html>
"""