import { EVENTS } from "./events.js";
import { set_text } from "./utils.js";

export class CombatLog {
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

		EVENTS.addEventListener("step", (v) => {
			if (v) {
				this.add_end_turn();
			}
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

	add_end_turn() {
		var cell = this.insertCell({type: "stepend", msg: "** The Turn has Ended **"});
	}

	addlog(msg, step=false) {
		//TABMANAGER.update_tab("printout");
		EVENTS.alert("update_tab", "printout");
		
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