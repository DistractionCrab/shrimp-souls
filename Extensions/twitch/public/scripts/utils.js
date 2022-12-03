import { EVENTS } from "./events.js";

export function clear_node(n) {
	n.innerHTML = "";
	return n;
}

export function set_text(n, s) {
	n.innerHTML = "";
	const sp = document.createElement("span");
	const t = document.createTextNode(s);
	sp.appendChild(t)
	n.appendChild(sp);
	return sp;
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


export class AlternatingCell {
	constructor(row) {
		this.cell = row.insertCell(row.cells.length);
		this.text = [];
		this.index = 0;

		this.cell.addEventListener("click", () => {
			console.log("click");
			if (this.text.length > 0) {
				this.text[this.index].classList.toggle("hidden", true);
				this.index = (this.index + 1) % this.text.length;
				this.text[this.index].classList.toggle("hidden", false);
			}
		});
	}

	add_text(txt) {
		const elem = document.createElement("div");
		set_text(elem, txt);

		this.text.push(elem);

		if (this.text.length === 1) {
			elem.classList.toggle("hidden", false);
		} else {
			elem.classList.toggle("hidden", true);
		}

		this.cell.appendChild(elem);
	}
}

export class TargetWatcher {
	constructor() {
		this.targeted = [];

		EVENTS.addEventListener("toggle_target", (en) => {
			for (const e of en) {
				const index = this.targeted.indexOf(e.name);

				if (index === -1) {
					this.targeted.push(e.name);
				} else {
					this.targeted.splice(index, 1);
				}
			}			
		});
	}
}