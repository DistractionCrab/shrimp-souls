import { Hub } from "hub.js";

export class Root {
	constructor(page, parent=null) {
		this.page = page;
		this.parent = parent;
		this.active = false;
	}
}



export function get_world_panel(t, root) {
	return new Hub(root);
}