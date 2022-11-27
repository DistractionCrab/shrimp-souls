import { EVENTS } from "./events.js";
import { set_text, AlternatingCell } from "./utils.js";
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

			const ncell = new AlternatingCell(row);
			//row.appendChild(ncell.cell);
			ncell.add_text(d.displayName);
			ncell.add_text(d.desc);
			ncell.text[0].classList.add("spellname");
			//var ncell = row.insertCell(1);
			//ncell.classList.add("spellname");
			//set_text(ncell, d.displayName);

			button.addEventListener("click", () => {
				//EVENTS.alert("server_message", MESSAGES.ability(d.name, this.targeted))
				CONFIRM.confirm(d.name, d.displayName, this.targeted, true)
			});
		}
	}
}

export class UseConfirm {
	constructor() {
		this.page = document.getElementById("abilityconfirm");
		this.targets = document.getElementById("confirmtargetlist");
		this.abi_name = document.getElementById("abilitynamespan");
		this.abi_confirm = document.getElementById("abilityconfirmbutton");
		this.abi_cancel = document.getElementById("abilitycancelbutton");
		this.page.classList.toggle("hidden");
		this.abi_or_item = true;

		this.abi_key = null;
		this.targets_list = [];

		this.abi_confirm.addEventListener("click", () => {
			if (this.abi_or_item) {
				EVENTS.alert("server_message", MESSAGES.ability(this.abi_key, this.targets_list))
			} else {
				EVENTS.alert("server_message", MESSAGES.item(this.abi_key, this.targets_list))
			}
			
			this.page.classList.toggle("hidden");
		});

		this.abi_cancel.addEventListener("click", () => {
			this.abi_key = null;
			this.targets_list = [];
			this.page.classList.toggle("hidden");
		});
	}

	confirm(abi, displayName, ts, aori) {
		this.abi_key = abi;
		this.targets_list = ts;
		this.page.classList.toggle("hidden");

		set_text(this.abi_name, displayName);

		this.targets.innerHTML = "";

		for (const t of ts) {
			const e = document.createElement("li");
			set_text(e, t);
			this.targets.appendChild(e);
		}

		this.abi_or_item = aori;
	}
}

export const CONFIRM = new UseConfirm();