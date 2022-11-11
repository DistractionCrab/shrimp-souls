import { EVENTS } from "./events.js";
import { set_text } from "./utils.js";
import { ABILITY_DATA } from "./classdata.js";
import { MESSAGES } from "./messages.js";

export class SpellBook {

	constructor() {
		this.spell_table = document.getElementById("spelltable");
		this.target_list = document.getElementById("targetlist");
		this.class_name = "default";
		this.targeted = [];

		EVENTS.addEventListener("charsheet", (data) => {
			const c = data['class'];
			if (c !== this.class_name) {
				this.class_name = c.toLowerCase();
				this.update();	
			}			
		});

		EVENTS.addEventListener("toggle_target", (en) => {
			for (const e of en) {
				this.toggle(e)
			}			
		});

		EVENTS.addEventListener("remove_npc", (data) => {
			for (const e of data) {
				this.remove(e)
			}
		});

		EVENTS.addEventListener("remove_player", (data) => {
			for (const e of data) {
				this.remove(e)
			}
		});
	}

	remove(name) {
		const tlist = document.getElementById("targetlist");
		const index = this.targeted.indexOf(name);

		if (index >= 0) {
			this.target_list.deleteRow(index);
			this.targeted.splice(index, 1);
		}
	}

	toggle(e) {
		const tlist = document.getElementById("targetlist");
		const index = this.targeted.indexOf(e.name);

		if (index < 0) {
			this.add_target(e);
			this.targeted.push(e.name);
		} else {
			this.target_list.deleteRow(index);
			this.targeted.splice(index, 1);
		}
	}

	add_target(e) {
		const row = this.target_list.insertRow(this.target_list.rows.length);
		const name = row.insertCell(0);
		set_text(name, e.name);

		const bcell = row.insertCell(1);
		const untarget = document.createElement("button");
		untarget.classList.add("untargetbutton");

		bcell.appendChild(untarget);

		untarget.addEventListener("click", (event) => {
			EVENTS.alert("toggle_target", [e]);
		});
	}

	update() {
		this.spell_table.innerHTML = "";
		var data = ABILITY_DATA[this.class_name];

		for (const d of data) {
			var row = this.spell_table.insertRow(0);
			row.classList.add("spellrow");
			var icell = row.insertCell(0);
			var button = document.createElement("button");
			icell.appendChild(button);
			button.classList.add("default_abilityicon");

			var ncell = row.insertCell(1);
			ncell.classList.add("spellname");
			set_text(ncell, d.displayName);

			button.addEventListener("click", () => {
				console.log(JSON.stringify(this.targeted));
				EVENTS.alert("server_message", MESSAGES.ability(d.name, this.targeted))
			});
		}
	}

}