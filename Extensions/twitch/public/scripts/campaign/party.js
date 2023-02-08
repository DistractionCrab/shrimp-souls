import { set_text } from "../utils.js";
import { EntityManager } from "../entity_manager.js";

function init_html(btext) {
	const button = document.createElement("button");
	button.textContent = btext;
	button.classList.add("tablinks");

	const party = document.createElement("div");
	const table = document.createElement("table");
	party.appendChild(table);
	party.classList.add("tabcontent");
	party.classList.add("scrollable");
	table.classList.add("spacedtable");

	return [button, party, table];
}

export class Party {
	constructor(btext="Party") {
		[this.button, this.content, this.table] = init_html(btext);
		this.entities = new EntityManager(this.table);
	}

	tab() {
		return { 
			button: this.button,
			content: this.content,
			active_fn: () => {},
			deactive_fn: () => {},
			campaign_view: this,
		}
	}

	update(data) {
		this.entities.update(data);
	}
}

export class NPCs extends Party {
	constructor() {
		super("NPCs");
	}
}