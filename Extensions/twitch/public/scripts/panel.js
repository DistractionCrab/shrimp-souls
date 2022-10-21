var log = window.Twitch ? window.Twitch.ext.rig.log : console.log;

const MESSAGES = {
	join: name => { return {msg: "join", userid: name} },
	action: () => { return {msg: "basicclassaction"} },
};


class CharSheet {
	constructor() {
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
		this.class_val = document.getElementById("class_value");
	}

	update_charsheet(msg) {		
		this.hp_val.innerHTML = `${msg['hp']}/${msg['max_hp']}`;
		this.xp_val.innerHTML = `${msg['xp']}/${msg['xp_req']}`;
		this.class_val.innerHTML = msg['class'];

		this.vigor_val.innerHTML = msg['attributes']['vigor'];
		this.endurance_val.innerHTML = msg['attributes']['endurance'];
		this.strength_val.innerHTML = msg['attributes']['strength'];
		this.dexterity_val.innerHTML = msg['attributes']['dexterity'];
		this.intelligence_val.innerHTML = msg['attributes']['intelligence'];
		this.faith_val.innerHTML = msg['attributes']['faith'];
		this.luck_val.innerHTML = msg['attributes']['luck'];
		this.perception_val.innerHTML = msg['attributes']['perception'];
	}
}

class CombatLog {
	constructor() {
		this.printout = document.getElementById("printout");
	}

	addlog(msg) {
		if (this.printout.rows.length > 10000) {
			this.printout.deleteRow(0);
		} else {
			var row = this.printout.insertRow(this.printout.rows.length);
			var cell = row.insertCell(0);
			cell.classList.add("printoutcell");
			cell.innerHTML = msg;
		}
	}
}

class EntityManager {
	constructor() {
		this.playerdisplay = document.getElementById("partytable");
		this.players = [];
	}

	updatePlayers(msg) {
		this.players = []
		while (this.playerdisplay.rows.length > 0) {
			this.playerdisplay.deleteRow(this.playerdisplay.rows.length-1);
		}

		for (const p of msg) {
			var row = this.playerdisplay.insertRow(0);
			var cell = row.insertCell(0);
			cell.innerHTML = `${p["name"]}: ${p["hp"]}/${p["max_hp"]}`;
		}
	}
}


class PageManager {
	constructor(testing) {		
		this.username = null;
		this.ocheck = false;		

		// Parts of the page to update the statuses.
		this.csheet = new CharSheet();
		this.printout = new CombatLog();
		this.enetities = new EntityManager();	

		// Socket setup.
		this.websocket = new WebSocket("ws://site.distractioncrab.net:443/");
		//this.websocket = new WebSocket("ws://localhost:80/");
		this.websocket.addEventListener("open", () => this.opened());
		this.websocket.addEventListener("message", ( {data}) => this.receive(data));	
		// Setup to attempt to connect.
		//setTimeout(() => MANAGER.setUName("distractioncrab"), 10000);
		this.joinid = setInterval(() => MANAGER.join(), 5000);		
	}

	join() {
		if (this.ocheck) {
			if (this.username) {
				clearInterval(this.joinid);
				this.websocket.send(JSON.stringify(MESSAGES.join(this.username)))		
			} else {
				log("Twitch has not provided username yet.")
			}
			
		} else {
			log("Attempted to join on closed socket.")
		}
		
		
	}

	setUName(name) {
		if (name == null) {
		} else {
			this.username = name;	
		}
		
	}

	receive(msg) {		
		//log("received message: " + msg);
		msg = JSON.parse(msg);
		if (msg["msg"] == "charsheet") {
			this.csheet.update_charsheet(msg['data']);
		} else if (msg["msg"] == "printout") {
			this.printout.addlog(msg["data"]);
		} else if (msg["msg"] == "partyinfo") {
			this.enetities.updatePlayers(msg["data"]);
		} else if (msg["msg"] == "update") {
			this.csheet.update_charsheet(msg['player']);
			this.printout.addlog(msg['data']);
			this.enetities.updatePlayers(msg['party']);
		}
	}

	opened() {
		this.ocheck = true;
		log("Established connection: site.distractioncrab.net")
	}

	initEvents() {
		this.websocket.addEventListener("open", this.opened);
		this.websocket.addEventListener("message", this.receive);
	}

	action() {
		log("Trying to action.");
		var msg = MESSAGES.action();
		this.websocket.send(JSON.stringify(msg));
	}
}

var MANAGER = new PageManager();



window.Twitch.ext.onAuthorized(
	function(auth){
		//log(auth);
		var parts=auth.token.split(".");
		var payload=JSON.parse(window.atob(parts[1]));
		if (payload.user_id) {
			MANAGER.setUName(payload.user_id);
			//log("id = " + payload.user_id);
		} else {
			//log("No ID given.");
			MANAGER.setUName(null);
		}
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

openTab(null, "charsheet")