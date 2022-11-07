const TESTING = true;

function log(s) {
	MANAGER.printout.addlog([s]);
}

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


const ABILITY_DATA = {
	milquetoast: [
	],
	knight: [
		{
			name: "block",
			displayName: "Block",
			targets: 0,
			icon: "default",
			desc: "Raise your shield to reduce incoming damage.",
		},
		{
			name: "cover",
			displayName: "Cover",
			targets: 1,
			icons: "default",
			desc: "Protect a target from harm, sacrificing your defenses."
		}
	],

	thief: [
		{
			name: "steal",
			displayName: "Steal",
			targets: 0,
			icon: "default",
			desc: "Attempt to steal from a nearby target.",
		},
		{
			name: "poach",
			displayName: "Poach",
			targets: 1,
			icons: "default",
			desc: "Attempt to poach a low-health enemy."
		}
	],

	assassin: [
		{
			name: "invis",
			displayName: "Shadowmeld",
			targets: 0,
			icon: "default",
			desc: "Becomes nearly invisible, and hard to detect.",
		},
		{
			name: "poison_blade",
			displayName: "Poison Blade",
			targets: 1,
			icons: "default",
			desc: "Attacks a target with your poisoned knife. Deals double damage while invisible."
		}
	],
	bard: [
		{
			name: "encourage",
			displayName: "War Ballad",
			targets: 0,
			icon: "default",
			desc: "Raise some party members' Att and Acc.",
		},
		{
			name: "charm",
			displayName: "Seductive Charisma",
			targets: 1,
			icons: "default",
			desc: "Attempts to charm an enemy, or reduce charm effects on an ally."
		}
	],
	cleric: [
		{
			name: "blessing",
			displayName: "Blessing of Iron",
			targets: 0,
			icon: "default",
			desc: "Raise some party memebers' defense.",
		},
		{
			name: "cleanse",
			displayName: "Cleanse",
			targets: 1,
			icons: "default",
			desc: "Remove negative effects from a taget."
		}
	],
	cryomancer: [
		{
			name: "chill",
			displayName: "Chilling Mist",
			targets: 0,
			icon: "default",
			desc: "Lowers some foes' attack and evasion.",
		},
		{
			name: "freeze",
			displayName: "Glaciate",
			targets: 1,
			icons: "default",
			desc: "Attempt to freeze a target for multiple turns."
		}
	],
	fencer: [
		{
			name: "ripstance",
			displayName: "En Garde",
			targets: 0,
			icon: "default",
			desc: "Enter a defensive and ready to parry an attacker.",
		},
		{
			name: "taunt",
			displayName: "Mocking Call",
			targets: 1,
			icons: "default",
			desc: "Attempt to taunt a target into attacking you."
		}
	],
	juggernaut: [
		{
			name: "warcry",
			displayName: "Battlecry",
			targets: 0,
			icon: "default",
			desc: "Emit a battlecry; Increasing some allies' Att.",
		},
		{
			name: "shatter",
			displayName: "Armor Shatter",
			targets: 1,
			icons: "default",
			desc: "Attack a target, shattering their armor and lowering their Def."
		}
	],
	priest: [
		{
			name: "prayer",
			displayName: "Healing Prayer",
			targets: 0,
			icon: "default",
			desc: "Utter a prayer, healing some allies for a small amount.",
		},
		{
			name: "heal",
			displayName: "Divine Touch",
			targets: 1,
			icons: "default",
			desc: "Revive a dead target or massively heal a living target.",
		}
	],
	paladin: [
		{
			name: "sealing",
			displayName: "Sealing Strikes",
			targets: 0,
			icon: "default",
			desc: "Enchant your weapon to stun targets that you strike.",
		},
		{
			name: "censure",
			displayName: "Divine Censure",
			targets: 1,
			icons: "default",
			desc: "Censure a target and reduce their scores."
		}
	],
	pyromancer: [
		{
			name: "pyroclasm",
			displayName: "Searing Steam",
			targets: 0,
			icon: "default",
			desc: "Release a cloud of steam and burn multiple foes.",
		},
		{
			name: "fireball",
			displayName: "Fireball",
			targets: 1,
			icons: "default",
			desc: "Throw a fireball at a target, dealing damage and burning them."
		}
	],

	sorcerer: [
		{
			name: "soulmass",
			displayName: "Conjure Phalanx",
			targets: 0,
			icon: "default",
			desc: "Conjure a retaliatory phalanx to retaliate against attackers.",
		},
		{
			name: "soulspear",
			displayName: "Soulspear",
			targets: 1,
			icons: "default",
			desc: "Conjure a magical spear to attack a foe and deal heavy damage."
		}
	],

	spellblade: [
		{
			name: "enchant",
			displayName: "Enchant Armaments",
			targets: 0,
			icon: "default",
			desc: "Enchant your sword and shield, increasing defense.",
		},
		{
			name: "magic_cover",
			displayName: "Magical Protection",
			targets: 1,
			icons: "default",
			desc: "Cover a target, increasing their defenses and granting them a magical phalanx. However your defenses are lowered."
		}
	],

	swordsman: [
		{
			name: "hamstring",
			displayName: "Hamstring",
			targets: 0,
			icon: "default",
			desc: "Create a whirl of your blades, and hamstring multiple foes.",
		},
		{
			name: "slice",
			displayName: "Heavy Slice",
			targets: 1,
			icons: "default",
			desc: "Slice into a target, dealing damage and inflicting bleed."
		}
	],
	warrior: [
		{
			name: "sharpen",
			displayName: "Grindstone",
			targets: 0,
			icon: "default",
			desc: "Sharpen your axe increasing your attack.",
		},
		{
			name: "armor_break",
			displayName: "Armor Break",
			targets: 1,
			icons: "default",
			desc: "Strike a target, breaking their armor and removing defensive statuses."
		}
	],

}

function clear_node(n) {
	n.innerHTML = "";
	return n;
}

function set_text(n, s) {
	n.innerHTML = "";
	n.appendChild(document.createTextNode(s));
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

		clear_node(this.hp_val).appendChild(document.createTextNode(`${msg['hp']}/${msg['max_hp']}`));
		clear_node(this.xp_val).appendChild(document.createTextNode(`${msg['xp']}/${msg['xp_req']}`));
		

		clear_node(this.vigor_val).appendChild(document.createTextNode(msg['attributes']['vigor']));
		clear_node(this.endurance_val).appendChild(document.createTextNode(msg['attributes']['endurance']));
		clear_node(this.strength_val).appendChild(document.createTextNode(msg['attributes']['strength']));
		clear_node(this.dexterity_val).appendChild(document.createTextNode(msg['attributes']['dexterity']));
		clear_node(this.intelligence_val).appendChild(document.createTextNode(msg['attributes']['intelligence']));
		clear_node(this.faith_val).appendChild(document.createTextNode(msg['attributes']['faith']));
		clear_node(this.luck_val).appendChild(document.createTextNode(msg['attributes']['luck']));
		clear_node(this.perception_val).appendChild(document.createTextNode(msg['attributes']['perception']));

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
		//this.timercell = this.insertCell()
		//this.timercell.setAttribute("id", "printouttimercell");
		this.timercell = document.getElementById("timertext");
		this.header = document.getElementById("printoutheader");
		this.filternames = {};
		this.filtertable = document.getElementById("filtertable");

		this.ttotal = 300;
		this.now = 0;

		const p = this;
		setInterval(function() {
				var now = new Date().getTime()/1000;
				var rem = p.ttotal - Math.abs(Math.floor((now - p.now)));

				if (rem <= 0) {
					p.refreshTimer("TURN ENDING SOON");
				} else {
					var min = Math.floor(rem/60);
					var s = Math.floor(rem % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
					p.refreshTimer(`Turn Ending in ${min}:${s}`);
				}
			},
			200);
	}

	apply_filters() {
		for (const r of this.printout.rows) {
			if (r.firstChild.classList.contains("stependcell")) {

			} else {
				var check = false;
				for (const [_, f] of Object.entries(this.filternames)) {

					if (f.cbox.checked) {
						if (r.firstChild.firstChild.textContent.includes(f.name)) {
							
							check = true;
							break;
						}
					}
				}	
				r.classList.toggle("hidden", !check);
			}
		}
		
	}

	add_filter_names(l, player) {
		for (const p of l) {
			if (!(p.name in this.filternames)) {
				var row = this.filtertable.insertRow(0);
				var ccell = row.insertCell(0);
				var label = row.insertCell(1);

				var cbox = document.createElement("input");
				cbox.setAttribute("type", "checkbox");
				cbox.classList.add("filtercheck");
				cbox.checked = true;
				set_text(label, p.name);

				ccell.appendChild(cbox);

				this.filternames[p.name] = {
					name: p.name,
					player: player, 
					npc: !player, 
					row: row,
					cbox: cbox,
				};
			}
		}
	}

	refreshTimer(s) {
		set_text(this.timercell, s);
	}

	updateTimer(msg) {
		this.ttotal = msg.ttotal;
		this.now = msg.now;
	}

	insertCell() {
		var row = this.printout.insertRow(this.printout.rows.length);
		var cell = row.insertCell(0);
		cell.classList.add("printoutcell");
		return cell;
	}

	addlog(msg, step=false) {
		if (this.printouttab.style.display !== "none") {
			this.header.classList.toggle("alerttab", true);	
		}
		
		
		if (this.printout.rows.length > 1000) {
			while (this.printout.rows.length > 1000 - msg.length) {
				this.printout.deleteRow(0);
			}				
		} else {
			
			for (const c of msg) {
				var cell = this.insertCell();
				set_text(cell, c);
			}
			if (step) {
				var cell = this.insertCell();
				cell.classList.add("stependcell");
				set_text(cell, "** The Turn has Ended **");
			}

			this.focus_recent();
			
		}

		//console.log(document.getElementById("printoutheader"));		
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
		clear_node(name).appendChild(document.createTextNode(this.data["name"]));
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

		if ("refreshEntities" in msg && msg["refreshEntities"]) {
			this.csheet.clear_target_selector();
			this.entities.clear();
		}

		if ("joined" in msg) {
			this.joined = msg['joined'];
			if (!msg["joined"]) {
				this.printout.join_message();
			}
		}
		if ("charsheet" in msg) {
			this.csheet.update_charsheet(msg['charsheet']);	
		}
		if ("log" in msg && this.joined) {
			this.printout.addlog(msg['log'], "step" in msg);
		}
		if ("partyinfo" in msg && this.joined) {
			this.entities.updatePlayers(msg['partyinfo']);
			this.printout.add_filter_names(msg["partyinfo"], true);
		}
		if ("npcinfo" in msg && this.joined) {
			this.entities.updateNPCS(msg["npcinfo"]);
			this.printout.add_filter_names(msg["npcinfo"], false);
		}
		
		if ("error" in msg) {
			log(msg['error']);
			this.printout.addlog(msg['error']);
			this.websocket.close();
		}

		if ("requestid" in msg && msg["requestid"]) {

			window.Twitch.ext.actions.requestIdShare();
			this.printout.addlog(["Please give access to your username to play this game."]);
		}

		if ("tinfo" in msg) {
			this.printout.updateTimer(msg["tinfo"]);
		}
		
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


window.Twitch.ext.onAuthorized(
	function(auth){
		MANAGER.setUName(auth);
	}
);


function openTab(evt, cityName) {
	// Declare all variables
	var i, tabcontent, tablinks;

	// Get all elements with class="tabcontent" and hide them
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Get all elements with class="tablinks" and remove the class "active"
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}

	// Show the current tab, and add an "active" class to the button that opened the tab
	document.getElementById(cityName).style.display = "block";
	if (evt) {
		evt.currentTarget.className += " active";
	}
}

openTab(null, "printouttab")

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

	log("Blurring");
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

document.getElementById("charsheetheader").addEventListener("click", (event) => { openTab(event, "charsheet"); });
document.getElementById("printoutheader").addEventListener("click", (event) => { 
	openTab(event, "printouttab");
	MANAGER.printout.focus_recent();
	event.currentTarget.classList.toggle("alerttab", false);
});
document.getElementById("partyheader").addEventListener("click", (event) => { openTab(event, "partytab"); });
document.getElementById("npcheader").addEventListener("click", (event) => { openTab(event, "npctab"); });
document.getElementById("abilityheader").addEventListener("click", (event) => { openTab(event, "abilitytab"); });
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