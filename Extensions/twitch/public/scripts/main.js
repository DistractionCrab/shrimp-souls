const TESTING = true;

import { ABILITY_DATA } from "./classdata.js";

function log(s) {
	MANAGER.printout.addlog([s]);
}

class EventSystem {
	addEventListener(name, fn) {
		if (!(name in this)) {
			this[name] = []
		}
		this[name].push(fn);
	}

	alert(name, data) {
		if (name in this) {
			for (const fn of this[name]) {
				fn(data);
			}
		}
	}
}

const EVENTS = new EventSystem();

const MESSAGES = {
	connect: name => { return {msg: "connect", jwt: name} },
	action: () => { return {msg: "basicclassaction"} },
	join: () => { return {msg: "join"}},
	ability: (sname, targets) => { 
		return { 
			msg: "ability",
			ability: sname,
			targets: targets,
		}
	},
	level: (att) => {
		return {
			msg: "levelup",
			att: att
		}
	},
	respec: (cl) => {
		return {
			msg: "respec",
			data: cl,
		}
	},
};



function clear_node(n) {
	n.innerHTML = "";
	return n;
}

function set_text(n, s) {
	n.innerHTML = "";
	n.appendChild(document.createTextNode(s));
	return n;
} 


class CharSheet {
	constructor() {
		this.xp_cur = 0;
		this.xp_req = 1;
		this.class_name = "default";

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
		this.target_selector = document.getElementById("targetselect");
		//log(this.target_selector);

		this.available_targets = new Set();

		EVENTS.addEventListener("refreshEntities", () => {
			this.clear_target_selector();
		})

		EVENTS.addEventListener("charsheet", (data) => {
			this.update_charsheet(data);
		})
	}

	update_spells() {
		var data = ABILITY_DATA[this.class_name];

		this.clear_targets();


		for (const d of data) {
			var row = this.spell_table.insertRow(0);
			row.classList.add("spellrow");
			var icell = row.insertCell(0);
			var button = document.createElement("button");
			icell.appendChild(button);
			button.classList.add("default_abilityicon");

			var ncell = row.insertCell(1);
			ncell.classList.add("spellname");
			clear_node(ncell).appendChild(document.createTextNode(d.displayName));

			//var dcell = row.insertCell(2);
			//dcell.appendChild(document.createTextNode(d.desc));

			var target_selector = this.target_selector;
			button.addEventListener("click", function() {
				var targets = [];
				for (const e of target_selector.options) {
					if (e.selected) {
						targets.push(e.value);
					}
				}
				//var selected = target_selector.options.filter(x => x.selected);
				MANAGER.sendMessage(MESSAGES.ability(d.name, targets));
			});
		}
	}

	clear_targets() {
		while (this.spell_table.rows.length > 0) {
			this.spell_table.deleteRow(0);
		}
	}

	add_target(t, p) {
		if (this.available_targets.has(t.name)) {
			return;
		}

		var e = document.createElement("option");
		e.value = t.name;
		if (p) {
			e.classList.add("playertarget");
		} else {
			e.classList.add("enemytarget");	
		}
		
		set_text(e, t.name);
		//clear_node(e).appendChild(document.createTextNode(t.name));

		this.target_selector.add(e);
		this.available_targets.add(t.name);
	}

	clear_target_selector() {
		this.available_targets = new Set();
		while (this.target_selector.firstChild) {
			this.target_selector.removeChild(this.target_selector.firstChild);
		}
	}

	remove_target(t) {
		this.available_targets.delete(t.name);

		var c = null;

		for (const child of this.target_selector.children) {
			if (child.nodeName == "OPTION") {
				if (child.value == t.name) {
					c = child;
					break;
				}
			}
		}

		this.target_selector.removeChild(c);
	}

	update_charsheet(msg) {
		this.ch_info = msg;
		this.xp_cur = msg['xp'];
		this.xp_req = msg['xp_req'];

		set_text(this.hp_val, `${msg['hp']}/${msg['max_hp']}`);
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
		//this.xp_bar.style.backgroundSize = 	`${propx}% 100%, 100% 100%`;

		for (const b of document.getElementsByClassName("lvlup")) {
			b.disabled = this.xp_cur < this.xp_req;
		}

		if (msg['class'] != this.class_name) {
			this.class_name = msg['class'].toLowerCase();
			this.update_spells();
		}
		this.class_name = msg['class'].toLowerCase();


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

class CombatLog {
	constructor() {
		this.printout = document.getElementById("printout");
		this.printouttab = document.getElementById("printouttab");
		this.printoutcontainer = document.getElementById("printoutcontainer");
		this.timercell = document.getElementById("timertext");
		this.header = document.getElementById("printoutheader");
		this.filternames = {};
		this.filtertable = document.getElementById("filtertable");
		this.max_rows = 1000;

		this.messages = [];

		this.ttotal = 300;
		this.now = 0;

		setInterval(() => {
				var now = new Date().getTime()/1000;
				var rem = this.ttotal - Math.abs(Math.floor((now - this.now)));

				if (rem <= 0) {
					set_text(this.timercell, "TURN ENDING SOON");
				} else {
					var min = Math.floor(rem/60);
					var s = Math.floor(rem % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
					set_text(this.timercell, `Turn Ending in ${min}:${s}`);
				}
			},
			200);

		this.insert_filter_field();

		document.getElementById("filterapplybutton").addEventListener("click", 
			(event) => {
				this.apply_filters();
			});

		EVENTS.addEventListener("joined", (joined) => {
			if (!joined) {
				this.join_message();
			}
		});

		EVENTS.addEventListener("log", (data) => {
			this.addlog(data);
		});

		EVENTS.addEventListener("error", (data) => {
			this.addlog(data);
		});

		EVENTS.addEventListener("tinfo", (data) => {
			this.updateTimer(data);
		});
	}

	str_to_msg(s) {
		if (typeof s == "string") {
			return { msg: s, type: "generic" }
		} else {
			return s;
		}
	}

	apply_filters() {
		const texts = []
		for (const r of document.getElementById("filtertable").rows) {
			texts.push(r.cells[1].firstChild.value);
		}


		for (const m of this.messages) {
			if (m.type == "generic") {
				if (texts.some((f) => m.msg.includes(f))) {
					m.cell.style.display = "block";
				} else {
					m.cell.style.display = "none";
				}
			} else if (m.type == "stepend") {

			}
		}		
	}

	insert_filter_field() {
		const table = document.getElementById("filtertable");
		const row = table.insertRow(table.rows.length);
		const cell = row.insertCell(0);
		set_text(cell, `Filter Text ${table.rows.length}: `);

		const cell2 = row.insertCell(1);
		const inp = document.createElement("input");
		inp.type = "text";
		inp.id = `filterinput${table.rows.length}`;
		inp.classList.add("filterinput");

		cell2.appendChild(inp);
	}


	refreshTimer(s) {
		set_text(this.timercell, s);
	}

	updateTimer(msg) {
		this.ttotal = msg.ttotal;
		this.now = msg.now;
	}

	insertCell(msg) {
		msg = this.str_to_msg(msg);
		var row = this.printout.insertRow(this.printout.rows.length);
		var cell = row.insertCell(0);

		cell.classList.add("printoutcell");
		if (msg.type == "stepend") {
			cell.classList.add("stependcell");
		}

		msg.cell = cell;
		set_text(cell, msg.msg);
		this.messages.push(msg);
		return cell;
	}

	addlog(msg, step=false) {
		TABMANAGER.update_tab("printout");		
		
		if (this.printout.rows.length > this.max_rows) {
			for (var i = 0; i < Math.ceil(this.max_rows/2); ++i) {
				this.printout.deleteRow(0);
			}

			this.messages = this.messages.splice(
				Math.ceil(this.max_rows/2), 
				this.printout.rows.length);
		}		

		for (const c of msg) {
			var cell = this.insertCell(c);
		}
		if (step) {
			var cell = this.insertCell({type: "stepend", msg: "** The Turn has Ended **"});
		}

		this.apply_filters();
		this.focus_recent();
	}

	focus_recent() {
		if (this.printoutcontainer.scrollHeight > this.printoutcontainer.clientHeight) {
			this.printoutcontainer.scrollTop = this.printoutcontainer.scrollHeight - this.printoutcontainer.clientHeight;
		}
	}

	join_message() {	
		var row = this.printout.insertRow(this.printout.rows.length);
		var cell = row.insertCell(0);
		cell.classList.add("printoutcell");


		const b = document.createElement("button");
		const t1 = document.createTextNode("Click ");
		const t2 = document.createTextNode(" to join the campaign and other chat members!");
		b.classList.add("joinbutton");
		b.addEventListener("click", function() { MANAGER.sendMessage(MESSAGES.join())});
		cell.appendChild(t1);
		cell.appendChild(b);
		cell.appendChild(t2);
	}
}


function entityStatusIcons(entity, table=null) {
	if (table === null) {
		table = document.createElement("table");
	} else {
		while (table.rows.length > 0) {
			table.deleteRow(0);
		}
	}
	
	var row1 = table.insertRow(0);

	const att = entity.status;
	for (const [k, v] of Object.entries(att)) {
		

		if (k == "taunt") {			
			if (v !== null) {
				//var cell = row1.insertCell(0);	
			}
		} else {			
			if (v > 0) {
				var cell = row1.insertCell(0);
				cell.classList.add(`${k}icon`);
				//cell.classList.add(`attupicon`);
			}
		}		
	}

	return table;
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
		
		//clear_node(name).appendChild(document.createTextNode(this.data["name"]));
		row1.insertCell(1);
		row1 = this.data_table.insertRow(1);
		var hpbar = row1.insertCell(0);
		
		var d = document.createElement("div");
		hpbar.appendChild(d);
		var prop = Math.max(0, Math.min(100, Math.ceil(this.data.hp/this.data.max_hp*100)));
		d.classList.add("healthbar");
		d.style.backgroundSize = `${prop}% 100%, 100% 100%`;

		var hpamt = row1.insertCell(1);
		hpamt.classList.add("hpamt");
		
		clear_node(hpamt).appendChild(document.createTextNode(`${this.data.hp} / ${this.data.max_hp}`));

		this.hp_bar = d;
		this.hp_display = hpamt;
	}

	update(data) {
		this.data = data;
		MANAGER.csheet.add_target(this.data, this.player);	

		var prop = Math.max(0, Math.min(100, Math.ceil(this.data.hp/this.data.max_hp*100)));
		this.hp_bar.style.backgroundSize = `${prop}% 100%, 100% 100%`;
		clear_node(this.hp_display).appendChild(document.createTextNode(`${this.data.hp} / ${this.data.max_hp}`));

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

class EntityManager {
	constructor() {
		this.playerdisplay = document.getElementById("partytable");
		this.npcdisplay = document.getElementById("npctable");
		this.players = {}
		this.npcs = {}

		EVENTS.addEventListener("refreshEntities", () => {
			this.clear();
		});

		EVENTS.addEventListener("partyinfo", (data) => {
			this.updatePlayers(data);
		});

		EVENTS.addEventListener("npcinfo", (data) => {
			this.updateNPCS(data);
		});
	}

	clear() {
		this.players = {};
		this.npcs = {}

		while (this.playerdisplay.rows.length > 0) {
			this.playerdisplay.deleteRow(0);
		}

		while (this.npcdisplay.rows.length > 0) {
			this.npcdisplay.deleteRow(0);
		}
	}

	updateNPCS(npcs) {
		for (const p of npcs) {
			if (!(p.name in this.npcs)) {
				const en = new Entity(p, false);
				this.npcs[p.name] = en

				var cell = this.npcdisplay.insertRow(0).insertCell(0);
				cell.classList.add("borderedcell");
				cell.appendChild(en.entity_table);
			}

			this.npcs[p.name].update(p);
		}
	}

	updatePlayers(players) {
		for (const p of players) {
			if (!(p.name in this.players)) {
				const en = new Entity(p, true);
				this.players[p.name] = en

				var cell = this.playerdisplay.insertRow(0).insertCell(0);
				cell.classList.add("borderedcell");
				cell.appendChild(en.entity_table);
			}

			this.players[p.name].update(p);
		}
		
	}
		
}


class PageManager {
	constructor(testing) {		
		this.username = null;
		this.joined = false;

		// Parts of the page to update the statuses.
		this.csheet = new CharSheet();
		this.printout = new CombatLog();
		this.entities = new EntityManager();

		this.reconnect = null;

		window.Twitch.ext.onAuthorized(
			(auth) => {
				this.setUName(auth);
			}
		);
	}

	init_socket() {
		if (this.username === null) {
			log("Tried to connect without username (This should not happen).");
		} else {
			if (TESTING) {
				this.websocket = new WebSocket(`ws://localhost:443/${this.username["channelId"]}`);	
			} else {
				this.websocket = new WebSocket(`wss://shrimpsouls.distractioncrab.net:443/${this.username["channelId"]}`);
			}
			
			
			this.websocket.addEventListener("open", () => this.opened());
			this.websocket.addEventListener("message", ({data}) => this.receive(data));
			this.websocket.addEventListener(
				"error", 
				(event) => {
					this.printout.addlog(["An error has happened, disconnecting..."]);
				});
			this.websocket.addEventListener("close", 
				(event) => {
					//log("Connection to server lost.");
					this.printout.addlog(["Connection to server lost."]);
					this.reconnect = setTimeout(() => { this.init_socket(); }, 20000);
				});
		}
	}


	setUName(name) {
		if (name === null) {
			// Nothing
		} else {
			this.username = name;
			this.init_socket();
		}
		
	}

	sendMessage(msg) {
		var s = JSON.stringify(msg)
		//log("Message to be sent: " + s);
		this.websocket.send(s);
		
	}

	receive(msg) {
		msg = JSON.parse(msg);

		for (const [k, v] of Object.entries(msg)) {
			EVENTS.alert(k, v)
		}

		if ("requestid" in msg && msg["requestid"]) {
			window.Twitch.ext.actions.requestIdShare();
		}
		if ("error" in msg) {
			this.websocket.close();
		}

		/*
		if ("refreshEntities" in msg && msg["refreshEntities"]) {
			//this.csheet.clear_target_selector();
			//this.entities.clear();
			EVENTS.alert("refreshEntities")
		}

		if ("joined" in msg) {
			//this.joined = msg['joined'];
			//if (!msg["joined"]) {
			//	this.printout.join_message();
			//}
			EVENTS.alert("joined", msg.joined);
		}
		if ("charsheet" in msg) {
			//this.csheet.update_charsheet(msg['charsheet']);	
			EVENTS.alert("charsheet", msg.charsheet);
		}

		if ("log" in msg) {
			//this.printout.addlog(msg['log'], "step" in msg);
			
			EVENTS.alert("log", msg.log);
		}
		if ("partyinfo" in msg) {
			//this.entities.updatePlayers(msg['partyinfo']);
			EVENTS.alert("partyinfo", msg.partyinfo)
		}
		if ("npcinfo" in msg) {
			//this.entities.updateNPCS(msg["npcinfo"]);
			EVENTS.alert("npcinfo", msg.npcinfo)
		}
		

		if ("tinfo" in msg) {
			//this.printout.updateTimer(msg["tinfo"]);
			EVENTS.alert("tinfo", msg.tinfo)
		}*/
		
	}

	level(att) {
		this.websocket.send(JSON.stringify(MESSAGES.level(att)))
	}

	opened() {
		this.printout.addlog(["Established connection to game server."]);
		if (this.reconnect !== null) {
			clearTimeout(this.reconnect);
		}
		this.websocket.send(JSON.stringify(MESSAGES.connect(this.username)))
	}

	action() {
		var msg = MESSAGES.action();
		this.websocket.send(JSON.stringify(msg));
	}
}

const MANAGER = new PageManager();



class TabManager {
	constructor(tabs) {
		this.tabs = tabs;
		this.init();
		//this.tabs = this.tabs.reduce((m, o) => { m[o.body] = o; return m}, {})
		//console.log(JSON.stringify(this.tabs));
		this.tabs.printout.button.click();


	}

	init() {
		for (const [_, e] of Object.entries(this.tabs)) {

			e.button = document.getElementById(e.header);
			e.button.addEventListener("click", (event) => {
				this.hide_tabs();
				e.content.style.display = "block";
				e.active = true;

				e.button.classList.toggle("alerttab", false);
				e.active_fn();
			});
			e.content = document.getElementById(e.body);
		}


	}

	hide_tabs() {
		for (const [_, e] of Object.entries(this.tabs)) {
			e.content.style.display = "none";
			e.active = false;
		}
	}

	is_active(name) {
		for (const [_, e] of Object.entries(this.tabs)) {
			if (e.body === name) {
				return e.active;
			}
		}
		return false;
	}

	update_tab(name) {
		if (name in this.tabs && !this.tabs[name].active) {
			this.tabs[name].button.classList.toggle("alerttab", true);
		}
	}
}

const TABMANAGER = new TabManager({
	charsheet: { 
		header: "charsheetheader",
		body: "charsheet", 
		active: false,
		active_fn: () => {},
		deactive_fn: () => {},
	},
	printout: { 
		header: "printoutheader", 
		body: "printouttab", 
		active: false,
		active_fn: () => { MANAGER.printout.focus_recent() },
		deactive_fn: () => {},
	},
	party: { 
		header: "partyheader", 
		body: "partytab", 
		active: false, 
		active_fn: () => {},
		deactive_fn: () => {},
	},
	npcs: { 
		header: "npcheader", 
		body: "npctab", 
		active: false, 
		active_fn: () => {},
		deactive_fn: () => {},
	},
	skills: { 
		header: "abilityheader", 
		body: "abilitytab", 
		active: false, 
		active_fn: () => {},
		deactive_fn: () => {},
	},
});


function expand_select(obj) {
	if (obj.size == 0) {
		obj.setAttribute("size", 5);
		obj.style.height="var(--classselect-opened)";
	} else {
		obj.size=0;
		obj.style.height="var(--class-select-height)";
	}
	
	//obj.click();

	//log("Expanding");
}

function blur_select(obj) {
	obj.size=0;
	obj.style.height="var(--class-select-height)";
}

function respec() {
	const obj = document.getElementById("classselect");
	MANAGER.sendMessage(MESSAGES.respec(obj.options[obj.selectedIndex].value))
}

function confirm_level(att) {
	if (confirm(`Do you wish to level ${att}?`)) {
		MANAGER.level(att);	
	}
}


document.getElementById("classselect").addEventListener("mousedown", (event) => { expand_select(event.target); });
//document.getElementById("classselect").addEventListener("change", (event) => { blur_select(event.target); });
document.getElementById("respecbutton").addEventListener("click", () => { respec(); });
document.getElementById("lvlup-vigor").addEventListener("click", () => { MANAGER.level("vigor"); });
document.getElementById("lvlup-endurance").addEventListener("click", () => { MANAGER.level("endurance"); });
document.getElementById("lvlup-strength").addEventListener("click", () => { MANAGER.level("strength"); });
document.getElementById("lvlup-dexterity").addEventListener("click", () => { MANAGER.level("dexterity"); });
document.getElementById("lvlup-intelligence").addEventListener("click", () => { MANAGER.level("intelligence"); });
document.getElementById("lvlup-faith").addEventListener("click", () => { MANAGER.level("faith"); });
document.getElementById("lvlup-luck").addEventListener("click", () => { MANAGER.level("luck"); });
document.getElementById("lvlup-perception").addEventListener("click", () => { MANAGER.level("perception"); });

// Setup click listeners for class options to close selection menus.
for (const c of document.getElementsByClassName("classoption")) {
	c.addEventListener("click", function(event) {
		const p = event.currentTarget.parentElement

		if (p.size > 0) {
			p.size=0;
			p.style.height="var(--class-select-height)";
		}
	});
}

/*
setInterval(function() {
	var popup = document.getElementById("myPopup");
  	popup.classList.toggle("show");
}, 5000);
*/

document.getElementById("filterbutton").addEventListener("click", () => {
	document.getElementById("filterpopup").classList.toggle("hidden");
});