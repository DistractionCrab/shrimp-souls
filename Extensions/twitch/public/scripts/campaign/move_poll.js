import { set_text } from "../utils.js";
import { EntityManager } from "../entity_manager.js";
import { MESSAGES } from "../messages.js";
import { EVENTS } from "../events.js";

function init_html() {
	const button = document.createElement("button");
	button.textContent = "Move";
	button.classList.add("tablinks");

	const party = document.createElement("div");
	party.innerHTML = HTML;

	//const bn = document.getElementById("move-north-vote");
	//const bs = document.getElementById("move-south-vote");
	//const be = document.getElementById("move-east-vote");
	//const bw = document.getElementById("move-west-vote");

	const bn = party.querySelector("#move-north-vote");
	const bs = party.querySelector("#move-south-vote");
	const be = party.querySelector("#move-east-vote");
	const bw = party.querySelector("#move-west-vote");

	bn.onclick = () => {
		EVENTS.alert("server_message", MESSAGES.action({
			"vote": "North"
		}))
	};
	bn.classList.add('act-button');
	bs.classList.add('act-button');
	be.classList.add('act-button');
	bw.classList.add('act-button');

	bs.onclick = () => {
		EVENTS.alert("server_message", MESSAGES.action({
			"vote": "South"
		}))
	};

	be.onclick = () => {
		EVENTS.alert("server_message", MESSAGES.action({
			"vote": "East"
		}))
	};

	bw.onclick = () => {
		EVENTS.alert("server_message", MESSAGES.action({
			"vote": "West"
		}))
	};

	return [button, party];
}

const HTML = `
	<table>
		<tr class="north-path-option">
			<td>
				Move North?
			</td>
			<td>
				<button id="move-north-vote">Vote for North</button>
			</td>
		</tr>
		<tr class="south-path-option">
			<td>
				Move South?
			</td>
			<td>
				<button id="move-south-vote">Vote for South</button>
			</td>
		</tr>
		<tr class="east-path-option">
			<td>
				Move East?
			</td>
			<td>
				<button id="move-east-vote">Vote for East</button>
			</td>
		</tr>
		<tr class="north-west-option">
			<td>
				Move West?
			</td>
			<td>
				<button id="move-west-vote">Vote for West</button>
			</td>
		</tr>
	</table>
`;

export class Poll {
	constructor() {
		[this.button, this.form] = init_html();
	}

	tab() {
		return { 
			button: this.button,
			content: this.form,
			active_fn: () => {},
			deactive_fn: () => {},
			campaign_view: this,
		}
	}

	update(data) {
	}
}
