import { EVENTS } from "../events.js";
import { Arena } from "./arena.js";

const C_MAPS = {
	"arena": Arena,
};


export class CampaignManager {
	constructor() {
		this.panel = document.getElementById("worldtab");
		this.current = null;
		EVENTS.addEventListener("campinfo", (data) => this.update(data));

	}

	update(data) {
		if (this.current === null || data.name !== this.current.name) {
			const c = C_MAPS[data.name];
			this.current = new c(this.panel);
			
		}
		if (this.current !== null) {
			this.current.update(data);	
		}
	}
}