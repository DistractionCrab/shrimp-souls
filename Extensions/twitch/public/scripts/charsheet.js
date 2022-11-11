import { EVENTS } from "./events.js";
import { set_text } from "./utils.js";

export class CharSheet {
	constructor() {
		this.xp_cur = 0;
		this.xp_req = 1;

		this.chinfo = {}

		this.vigor_val = document.getElementById("vigor_value");
		this.endurance_val = document.getElementById("endurance_value");
		this.strength_val = document.getElementById("strength_value");
		this.dexterity_val = document.getElementById("dexterity_value");
		this.intelligence_val = document.getElementById("intelligence_value");
		this.faith_val = document.getElementById("faith_value");
		this.luck_val = document.getElementById("luck_value");
		this.perception_val = document.getElementById("perception_value");

		this.hp_val = document.getElementById("hp_value");
		this.xp_val = document.getElementById("xp_value");
		this.class_val = document.getElementById("classselect");

		this.hp_bar = document.getElementById("player_healthbar");
		this.statusdisplay = document.getElementById("playerstatus");
		//this.xp_bar = document.getElementById("player_xpbar");

		this.spell_table = document.getElementById("spelltable");

		EVENTS.addEventListener("charsheet", (data) => {
			this.update_charsheet(data);
		});
	}

	update_charsheet(msg) {
		this.ch_info = msg;
		this.xp_cur = msg['xp'];
		this.xp_req = msg['xp_req'];

		set_text(this.hp_val, `${msg.hp}/${msg.max_hp}`);
		set_text(this.xp_val, `${msg['xp']}/${msg['xp_req']}`);
		

		set_text(this.vigor_val, msg['attributes']['vigor']);
		set_text(this.endurance_val, msg['attributes']['endurance']);
		set_text(this.strength_val, msg['attributes']['strength']);
		set_text(this.dexterity_val, msg['attributes']['dexterity']);
		set_text(this.intelligence_val, msg['attributes']['intelligence']);
		set_text(this.faith_val, msg['attributes']['faith']);
		set_text(this.luck_val, msg['attributes']['luck']);
		set_text(this.perception_val, msg['attributes']['perception']);

		var prop = Math.max(0, Math.min(100, Math.ceil(msg['hp']/msg['max_hp']*100)));
		var propx = Math.max(0, Math.min(100, Math.ceil(msg['xp']/msg['xp_req']*100)));

		this.hp_bar.style.backgroundSize = `${prop}% 100%, 100% 100%`;

		for (const b of document.getElementsByClassName("lvlup")) {
			b.disabled = this.xp_cur < this.xp_req;
		}


		this.update_status(msg);

		// Update class value.
		const obj = document.getElementById("classselect");
		const i = [...obj.options].findIndex((v) => { return v.value == this.class_name});
		this.class_val.selectedIndex = i;
	}

	update_status(data) {
		while (this.statusdisplay.rows.length > 0) {
			this.statusdisplay.deleteRow(0);
		}

		const kv = Object.entries(data.status);
		var ct = 0;
		var row = this.statusdisplay.insertRow(0);
		for (const [k, v] of kv) {
			if (ct > 8) {
				row = this.statusdisplay.insertRow(0);
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