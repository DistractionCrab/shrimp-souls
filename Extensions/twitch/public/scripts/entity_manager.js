
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

	table.replaceChildren(...elems);
}

class Entity {
	constructor(data) {
		this.data = data;
		this.status_table = document.createElement("table");
		this.data_table = document.createElement("table");
		this.entity_table = document.createElement("table");
		this.name = data["name"];

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
	constructor(display) {
		this.playerdisplay = display
		this.players = {};
		this.targeted = {};
		this.target_q = new Set();
		this.containers = {}

		EVENTS.addEventListener("toggle_target", (e) => {			
			for (const en of e) {
				this.toggle_target(en, en.name in this.players);
			}			
		})
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

		for (const n of names) {
			if (n in this.target_q) {
				delete this.target_q[n];
			}
		}
	}

	toggle_target(e, player) {
		if (!(e.name in this.containers)) {
			return;
		}
		
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
		this.playerdisplay.innerHTML = "";
	}

	insert_row(p) {
		const en = new Entity(p);
		const t = this.playerdisplay;

		var row = t.insertRow(t.rows.length);
		row.name = p.name;
		var cell = row.insertCell(0);
		cell.classList.add("borderedcell");	
		
		cell.appendChild(en.entity_table);
		en.update(p);

		this.containers[p.name] = cell;



		return en;

	}
	

	update(players) {
		for (const p of players) {
			if (!(p.name in this.players)) {
				this.players[p.name] = this.insert_row(p, true);
			} else {
				this.players[p.name].update(p);
			}
		}
		sort_table(this.playerdisplay, this.target_q);		
	}
		
}