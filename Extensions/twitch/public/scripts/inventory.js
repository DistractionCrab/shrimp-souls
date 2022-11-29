import { EVENTS } from "./events.js";
import { AlternatingCell, TargetWatcher } from "./utils.js";
import { CONFIRM } from "./spellbook.js";

export class Inventory extends TargetWatcher {
	constructor() {
		super();
		this.table = document.getElementById("inventory");

		EVENTS.addEventListener("charsheet", (data) => {
			this.update(data);
		});
	}

	update(data) {

		this.table.innerHTML = "";
		if ("inventory" in data) {
			var index = 0;
			for (const a of data.inventory) {
				const r = this.table.insertRow(this.table.rows.length);
				r.classList.add("spellrow")
				var icell = r.insertCell(0);
				var button = document.createElement("button");
				icell.appendChild(button);
				button.classList.add("default_abilityicon");

				const i_index = index;
				button.addEventListener("click", () => {
					CONFIRM.confirm(i_index, a, this.targeted, false)
				});

				const c = new AlternatingCell(r);
				c.add_text(a);
				c.text[0].classList.add("spellname");
				index += 1;

			}
		}
	}
}