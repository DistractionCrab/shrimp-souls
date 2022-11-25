import { EVENTS } from "./events.js";
import { AlternatingCell } from "./utils.js";

export class Inventory {
	constructor() {
		this.table = document.getElementById("inventory");

		EVENTS.addEventListener("charsheet", (data) => {
			this.update(data);
		});
	}

	update(data) {
		this.table.innerHTML = "";
		if ("inventory" in data) {
			for (const a of data.inventory) {
				const r = this.table.insertRow(this.table.rows.length);
				var icell = row.insertCell(0);
				var button = document.createElement("button");
				icell.appendChild(button);
				button.classList.add("default_abilityicon");


				const c = new AlternatingCell(r);
				c.add_text(a);

			}
		}
	}
}