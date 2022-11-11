
import { EVENTS } from "./events.js";
import { set_text } from "./utils.js";

function compare(a, b) {
	// Both are targeted.
	if (a[1] && b[1]) {
		return a[0].name.localeCompare(b[0].name);
	} else if (a[1]) {
		return -1;
	} else if (b[1]) {
		return 1;
	} else {
		return a[0].name.localeCompare(b[0].name);
	}
}


function sort_table(table, target_q) {
	//for (const r of table.rows) {
	//	console.log(r.name);
	//}
	//console.log("---------------------------");
	const elems = [].slice.call(table.rows);
	elems.sort((r1, r2) => {
		if (target_q.has(r1.name) && target_q.has(r2.name)) {
			return r1.name.localeCompare(r2.name);
		} else if (target_q.has(r1.name)) {
			return -1;
		} else if (target_q.has(r2.name)) {
			return 1;
		} else {
			return r1.name.localeCompare(r2.name);
		}
	});

	//for (const r of table.rows) {
	//	console.log(r.name);
	//}
	//console.log("---------------------------");

	table.replaceChildren(...elems);
}

class Entity {
	constructor(data, player) {
		this.data = data;
		this.status_table = document.createElement("table");
		this.data_table = document.createElement("table");
		this.entity_table = document.createElement("table");
		this.name = data["name"];
		this.player = player;

		this.init_table();		
	}


	init_table() {
		var row = this.entity_table.insertRow(0);
		var cell = row.insertCell(0);
		cell.appendChild(this.data_table)
		row = this.entity_table.insertRow(1);
		cell = row.insertCell(0);
		cell.appendChild(this.status_table);
		


		// update data_table
		var row1 = this.data_table.insertRow(0);

		var name = row1.insertCell(0);
		name.classList.add("name-cell");
		if (this.player) {
			set_text(name, `${this.data.name} (${this.data["class"]})`)
		} else {
			set_text(name, this.data.name);
		}
		
		var t = row1.insertCell(1);
		var button = document.createElement("button");
		button.classList.add("targetbutton");
		t.appendChild(button);
		button.addEventListener("click", () => {
			EVENTS.alert("toggle_target", [this.data]);
		})


		row1 = this.data_table.insertRow(1);
		var hpbar = row1.insertCell(0);
		
		var d = document.createElement("div");
		hpbar.appendChild(d);
		var prop = Math.max(0, Math.min(100, Math.ceil(this.data.hp/this.data.max_hp*100)));
		d.classList.add("healthbar");
		d.style.backgroundSize = `${prop}% 100%, 100% 100%`;

		var hpamt = row1.insertCell(1);
		hpamt.classList.add("hpamt");
		
		set_text(hpamt, `${this.data.hp} / ${this.data.max_hp}`);

		this.hp_bar = d;
		this.hp_display = hpamt;
	}

	update(data) {
		this.data = data;

		var prop = Math.max(0, Math.min(100, Math.ceil(this.data.hp/this.data.max_hp*100)));
		this.hp_bar.style.backgroundSize = `${prop}% 100%, 100% 100%`;
		set_text(this.hp_display, `${this.data.hp} / ${this.data.max_hp}`);

		// Update status
		while (this.status_table.rows.length > 0) {
			this.status_table.deleteRow(0);
		}

		const kv = Object.entries(this.data.status);
		var ct = 0;
		var row = this.status_table.insertRow(0);
		for (const [k, v] of kv) {
			if (ct > 8) {
				row = this.status_table.insertRow(0);
			}

			if (k == "taunt") {			
				if (v !== null) {
					ct += 1;
				}
			} else {			
				if (v > 0) {
					var cell = row.insertCell(0);
					cell.classList.add(`${k}icon`);
					ct += 1;
				}
			}		
		}
	}
}

export class EntityManager {
	constructor() {
		this.playerdisplay = document.getElementById("partytable");
		this.npcdisplay = document.getElementById("npctable");
		this.players = {};
		this.npcs = {};
		this.p_index = [];
		this.n_index = [];
		this.targeted = {};

		this.target_q = new Set();
		this.containers = {}


		EVENTS.addEventListener("partyinfo", (data) => {
			this.updatePlayers(data);
		});

		EVENTS.addEventListener("npcinfo", (data) => {
			this.updateNPCS(data);
		});

		EVENTS.addEventListener("remove_npc", (data) => {
			this.remove(data);
		});

		EVENTS.addEventListener("remove_player", (data) => {
			this.remove(data);
		});

		EVENTS.addEventListener("toggle_target", (e) => {
			
			for (const en of e) {
				this.toggle_target(en, en.name in this.players);
			}
			
		})
	}

	is_player(name) {
		return name in this.players;
	}

	is_npc(name) {
		return name in this.npcs;
	}

	get_structs(name) {
		if (name in this.npcs) {
			return [this.n_index, this.npcs, this.npcdisplay];
		} else if (name in this.players) {
			return [this.p_index, this.players, this.playerdisplay];
		} else {
			return null;
		}
	}

	remove(names) {
		for (var i = this.playerdisplay.rows.length - 1; i >= 0; -- i) {
			const n = this.playerdisplay.rows[i].name;

			if (names.includes(n)) {
				this.playerdisplay.deleteRow(i);
				delete this.players[n];
				delete this.containers[n]
			}
		}

		for (var i = this.npcdisplay.rows.length - 1; i >= 0; -- i) {
			const n = this.npcdisplay.rows[i].name;
			if (names.includes(n)) {
				this.npcdisplay.deleteRow(i);
				delete this.npcs[n];
				delete this.containers[n]
			}
		}

		for (const n of names) {
			if (n in this.target_q) {
				delete this.target_q[n];
			}
		}
	}

	toggle_target(e, player) {
		
		if (this.target_q.has(e.name)) {
			this.target_q.delete(e.name);

			this.containers[e.name].classList.toggle("borderedcell", true);
			this.containers[e.name].classList.toggle("targetedcell", false);
		} else {
			this.target_q.add(e.name);

			this.containers[e.name].classList.toggle("borderedcell", false);
			this.containers[e.name].classList.toggle("targetedcell", true);
		}
	}

	clear() {
		this.players = {};
		this.npcs = {}
		this.p_index = [];
		this.n_index = []
		this.playerdisplay.innerHTML = "";
		this.npcdisplay.innerHTML = "";
	}

	insert_row(p, player) {
		const en = new Entity(p, player);
		const t = player ? this.playerdisplay : this.npcdisplay;

		var row = t.insertRow(t.rows.length);
		row.name = p.name;
		var cell = row.insertCell(0);
		cell.classList.add("borderedcell");	
		
		cell.appendChild(en.entity_table);
		en.update(p);

		this.containers[p.name] = cell;



		return en;

	}
	

	updateNPCS(npcs) {
		for (const p of npcs) {
			if (!(p.name in this.npcs)) {
				//this.insert_row(this.npcdisplay, this.npcs, this.n_index, p, false);
				this.npcs[p.name] = this.insert_row(p, false);
			} else {
				this.npcs[p.name].update(p);
			}
		}

		sort_table(this.npcdisplay, this.target_q);
	}

	updatePlayers(players) {
		for (const p of players) {
			if (!(p.name in this.players)) {
				this.players[p.name] = this.insert_row(p, true);
				//this.insert_row(this.playerdisplay, this.players, this.p_index, p, true);
			} else {
				this.players[p.name].update(p);
			}
		}
		sort_table(this.playerdisplay, this.target_q);
		
	}
		
}