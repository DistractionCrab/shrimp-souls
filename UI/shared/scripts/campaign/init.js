import { EVENTS } from "../events.js";
import { TabManager } from "../utils.js";
import { Party, NPCs } from "./party.js";
import { Map } from "./map.js";
import { Poll } from "./move_poll.js";

const DATA_MAP = {
	party: Party,
	npcs: NPCs,
	map: Map,
	move_poll: Poll,
}

export class CampaignManager {
	constructor() {
		this.panel = document.getElementById("worldtab");
		this.tabs = document.getElementById("worldtabsections");
		this.manager = new TabManager({});
		
		EVENTS.addEventListener("campinfo", (data) => this.update(data));

	}

	update(data) {
		//console.log(`${JSON.stringify(data, null, 4)} is the data`);
		
		for (const [k, v] of Object.entries(data)) {			
			if (k in DATA_MAP) {
				this.convey(k, v);
			}
		}

		for (const [k, _] of Object.entries(this.manager.tabs)) {
			if (!(k in DATA_MAP)) {
				this.manager.rem_tab(k);
			}
		}
	}

	convey(name, data) {
		if (data !== null) {
			if (!this.manager.has_tab(name)) {
				const obj = new DATA_MAP[name]();
				this.manager.add_tab(name, obj.tab());
				const data = this.manager.get_tab(name);

				this.tabs.appendChild(data.button);
				this.panel.appendChild(data.content);
			}

			const t = this.manager.get_tab(name);
			t.campaign_view.update(data);	
		}
		
	}
}