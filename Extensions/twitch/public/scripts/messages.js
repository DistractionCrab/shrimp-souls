export const MESSAGES = {
	connect: name => { return {msg: "connect", jwt: name} },
	action: () => { return {msg: "basicclassaction"} },
	join: () => { return {msg: "join"}},
	ability: (sname, targets) => { 
		return { 
			msg: "ability",
			ability: sname,
			targets: targets,
		}
	},
	item: (index, targets) => { 
		return { 
			msg: "item",
			index: index,
			targets: targets,
		}
	},
	level: (att) => {
		return {
			msg: "levelup",
			att: att
		}
	},
	respec: (cl) => {
		return {
			msg: "respec",
			data: cl,
		}
	},
	action: (data) => {
		return {
			msg: "action",
			action: data,
		}
	},
};