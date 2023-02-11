function dragElement(elmnt, drag) {
	elmnt.onmousedown = dragMouseDown;
	var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
	function dragMouseDown(e) {
		e = e || window.event;
		e.preventDefault();
		// get the mouse cursor position at startup:
		pos3 = e.clientX;
		pos4 = e.clientY;
		document.onmouseup = closeDragElement;
		// call a function whenever the cursor moves:
		document.onmousemove = elementDrag;
	}

	function elementDrag(e) {
		e = e || window.event;
		e.preventDefault();
		// calculate the new cursor position:
		pos1 = pos3 - e.clientX;
		pos2 = pos4 - e.clientY;
		pos3 = e.clientX;
		pos4 = e.clientY;
		// set the element's new position:

		drag.style.top = (drag.offsetTop - pos2) + "px";
		drag.style.left = (drag.offsetLeft - pos1) + "px";
	}

	function closeDragElement() {
		// stop moving when mouse button is released:
		document.onmouseup = null;
		document.onmousemove = null;
	}
}

function init_html() {
	const button = document.createElement("button");
	button.textContent = "Map";
	button.classList.add("tablinks");

	const mapdiv = document.createElement("div");
	const dragdiv = document.createElement("div");
	const grid = document.createElement("table");
	mapdiv.appendChild(dragdiv);
	dragdiv.appendChild(grid);
	mapdiv.classList.add("tabcontent");
	dragdiv.classList.add("map-drag-cell");

	dragdiv.classList.add("draggable");

	return [button, mapdiv, dragdiv, grid];
}

export class Map {
	constructor(btext="Party") {
		[this.button, this.div, this.drag, this.grid] = init_html();
		this.index = [];
		this.rooms = {};
		this.location = null;
		this.uid = null;
		this.width = null;
		this.mapgrid = null;

		dragElement(this.div, this.drag);
	}

	tab() {
		return { 
			button: this.button,
			content: this.div,
			active_fn: () => {},
			deactive_fn: () => {},
			campaign_view: this,
		}
	}

	init_grid(data) {
		this.uid = data.uid;
		this.width = data.width;
		this.location = data.location;
		this.grid.replaceChildren();
		this.mapgrid = new Array(data.room_index.length).fill(null);

		// Initialize the total grid
		for (var i = 0; i < 2*data.width + 1; ++i) {
			const r = this.grid.insertRow(i);
			for (var k = 0; k < 2*data.width + 1; ++k) {					
				r.insertCell(k).classList.add("map-grid-cell");

			}
		}

		const [x, y] = this.location;
		this.grid.rows[2*y+1].cells[2*x+1].classList.toggle("current-location", true);

		// Initialize the room grid
		for (const [i, loc] of data.room_index.entries()) {
			const r = data.rooms[i];
			const x = 2*loc[0] + 1;
			const y = 2*loc[1] + 1;
			this.mapgrid[i] = new RTYPE_MAP[r.rtype](this.grid.rows[y].cells[x]);

			var cx = loc[0] + 1;
			var cy = loc[1]
			if (adjacent(i, [cx, cy], data)) {
				const c = this.grid.rows[y].cells[x+1];
				c.classList.add("horizontal_connector");
			}

			cx = loc[0];
			cy = loc[1] + 1
			if (adjacent(i, [cx, cy], data)) {
				const c = this.grid.rows[y+1].cells[x];
				c.classList.add("vertical_connector");
			}
		}
	}

	update(data) {
		if (this.uid !== data.uid) {			
			this.init_grid(data);
		} else {
			var [x, y] = this.location;
			this.grid.rows[2*y+1].cells[2*x+1].classList.toggle("current-location", false);

			this.location = data.location
			var [x, y] = this.location;
			this.grid.rows[2*y+1].cells[2*x+1].classList.toggle("current-location", true);
		}
	}
}

function adjacent(r1, r2, data) {
	if (r2[0] >= data.width || r2[1] >= data.width) {
		return false;
	}
	const edges = data.paths[r1];
	for (const e of edges) {
		if (e[0] === r2[0] && e[1] === r2[1]) {
			return true;
		}
	}
	return false;
}

class EmptyRoom {
	constructor(cell) {
		cell.classList.add("empty-room-cell");
	}
}

class CombatRoom {
	constructor(cell) {
		cell.classList.add("combat-room-cell");
	}
}

class VertConnector {
	constructor(cell) {

	}
}

class HoriConnector{
	constructor(cell) {

	}
}

const RTYPE_MAP = {
	empty: EmptyRoom,
	combat: CombatRoom,
};


function array_equiv(a1, a2) {
	if (a1.length === a2.length) {
		for (var i = 0; i < a1.length; ++i) {
			if (a1[i] !== a2[i]) {
				return false
			}
		}
		return true;
	}

	return false;
}