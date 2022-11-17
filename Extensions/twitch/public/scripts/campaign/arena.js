import { TabManager } from "../utils.js";
import { EntityManager } from "../entity_manager.js";

const HTML = `
<div class="tabsection">
	<button class="tablinks" id="homeheader">Home</button>
	<button class="tablinks" id="partyheader">Party</button>
	<button class="tablinks" id="npcheader">NPCs</button>
</div>
<div id="hometab">
	Welcome to the arena, this is the temporary autobattler for this game until other
	things are made. 
</div>
<div id="partytab">
	<table id="partytable">

	</table>
</div>
<div id="npctab">
	<table id="npctable">

	</table>
</div>
`;

export class Arena {
	constructor(panel) {
		this.name = "arena";
		this.panel = panel;
		panel.innerHTML = HTML;
		this.tabs = new TabManager(
			{
				main: { 
					header: "homeheader",
					body: "hometab", 
					active: false,
					active_fn: () => {},
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
			},
			"main");

		this.partyinfo = new EntityManager(document.getElementById("partytable"));
		this.npcinfo = new EntityManager(document.getElementById("npctable"));
	}

	update(data) {
		if (data.party !== null && data.party !== undefined) {
			this.partyinfo.update(data.party);
		}

		if (data.npcs !== null && data.npcs !== undefined) {
			this.npcinfo.update(data.npcs);
		}

		if ("clearNPCs" in data && data.clearNPCs) {
			this.npcinfo.clear()
		}
	}
}
