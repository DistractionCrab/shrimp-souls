const TESTING = false;

import { EVENTS } from "./events.js";
import { set_text, TabManager } from "./utils.js";
import { CombatLog } from "./combatlog.js";
import { SpellBook } from "./spellbook.js";
import { CharSheet } from "./charsheet.js";
import { EntityManager } from "./entity_manager.js";
import { MESSAGES } from "./messages.js";

class PageManager {
	constructor(testing) {		
		this.username = null;
		this.joined = false;

		// Parts of the page to update the statuses.
		this.csheet = new CharSheet();
		this.printout = new CombatLog();
		this.entities = new EntityManager();
		this.spellbook = new SpellBook();

		this.reconnect = null;
		this.websocket = null;

		window.Twitch.ext.onAuthorized(
			(auth) => {
				this.setUName(auth);
			}
		);

		EVENTS.addEventListener("server_message", (data) => {
			this.sendMessage(data);
		})
	}

	init_socket() {		
		if (this.websocket === null) {
			if (this.username === null) {
				console.log("Tried to connect without username (This should not happen).");
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
						this.websocket = null;
					});
				this.websocket.addEventListener("close", 
					(event) => {
						this.printout.addlog(["Connection to server lost."]);
						this.websocket = null;
						this.reconnect = setTimeout(() => { this.init_socket(); }, 20000);
					});
			}
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
},
"printout");


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