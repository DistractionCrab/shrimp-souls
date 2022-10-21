window.Twitch.ext.rig.log("Waffles");
var log = window.Twitch ? window.Twitch.ext.rig.log : console.log;

const MESSAGES = {
	join: name => { return {msg: "join", name: name} }
};



class PageManager {
	constructor(testing) {		
		this.username = null;
		this.ocheck = false;
		

		// Parts of the page to update the statuses.

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


		// Socket setup.
		this.websocket = new WebSocket("ws://site.distractioncrab.net/");
		//this.websocket = new WebSocket("ws://localhost:80/");
		this.websocket.addEventListener("open", () => this.opened());
		this.websocket.addEventListener("message", ( {data}) => this.receive(data));	
		// Setup to attempt to connect.
		//setTimeout(() => NETWORKLISTENER.setUName("distractioncrab"), 10000);
		this.joinid = setInterval(() => NETWORKLISTENER.join(), 5000);		
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
		this.username = name;
	}

	receive(msg) {		
		log("received message: " + msg);
		msg = JSON.parse(msg);
		if (msg["msg"] == "charsheet") {
			this.update_charsheet(msg);
		}
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

	opened() {
		this.ocheck = true;
		log("Established connection: site.distractioncrab.net")
	}

	initEvents() {
		this.websocket.addEventListener("open", this.opened);
		this.websocket.addEventListener("message", this.receive);
	}
}

var NETWORKLISTENER = new PageManager();



window.Twitch.ext.onAuthorized(
	function(auth){
		console.log("being called");
		var parts=auth.token.split(".");
		var payload=JSON.parse(window.atob(parts[1]));
		if (payload.user_id) {
			//MANAGER.setUName(payload.user_id);
			console.log(payload.user_id);
			// user has granted
			//jQuery.get('https://api.twitch.tv/kraken/users/' + payload.user_id, <etc>
		} else {
			// user has NOT granted
		}
	}
);

log(window.Twitch.ext.viewer.id);