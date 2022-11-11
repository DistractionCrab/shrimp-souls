class EventSystem {
	addEventListener(name, fn) {
		if (!(name in this)) {
			this[name] = []
		}
		this[name].push(fn);
	}

	alert(name, data) {
		if (name in this) {
			for (const fn of this[name]) {
				fn(data);
			}
		}
	}
}

export const EVENTS = new EventSystem();