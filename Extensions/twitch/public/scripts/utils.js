import { EVENTS } from "./events.js";

export function clear_node(n) {
	n.innerHTML = "";
	return n;
}

export function set_text(n, s) {
	n.innerHTML = "";
	n.appendChild(document.createTextNode(s));
	return n;
} 

export class TabManager {
	constructor(tabs, dtab) {
		this.tabs = tabs;
		this.init();
		this.tabs[dtab].button.click();

		EVENTS.addEventListener("update_tab", (name) => this.update_tab(name));
	}

	init() {
		for (const [_, e] of Object.entries(this.tabs)) {

			e.button = document.getElementById(e.header);
			e.button.addEventListener("click", (event) => {
				this.hide_tabs();
				e.content.style.display = "block";
				e.active = true;

				e.button.classList.toggle("alerttab", false);
				e.active_fn();
			});
			e.content = document.getElementById(e.body);
		}


	}

	hide_tabs() {
		for (const [_, e] of Object.entries(this.tabs)) {
			e.content.style.display = "none";
			e.active = false;
		}
	}

	is_active(name) {
		for (const [_, e] of Object.entries(this.tabs)) {
			if (e.body === name) {
				return e.active;
			}
		}
		return false;
	}

	update_tab(name) {
		if (name in this.tabs && !this.tabs[name].active) {
			this.tabs[name].button.classList.toggle("alerttab", true);
		}
	}
}