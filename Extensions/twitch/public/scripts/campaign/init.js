import { EVENTS } from "../events.js";
import { TabManager } from "../utils.js";
import { Party, NPCs } from "./party.js";

const DATA_MAP = {
	party: Party,
	npcs: NPCs
}

export class CampaignManager {
	constructor() {
		this.panel = document.getElementById("worldtab");
		this.tabs = document.getElementById("worldtabsections");
		this.manager = new TabManager({});
		
		EVENTS.addEventListener("campinfo", (data) => this.update(data));

	}

	update(data) {
		for (const [k, v] of Object.entries(data)) {
			//console.log(`[${k}, ${JSON.stringify(v)}] is the data`)
			if (k in DATA_MAP) {
				this.convey(k, v);
			}
		}
	}

	convey(name, data) {
		if (data === null) {
			this.manager.rem_tab(name);
		} else {
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