
export const ABILITY_DATA = {
	milquetoast: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
	],
	knight: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "block",
			displayName: "Block",
			targets: 0,
			icon: "default",
			desc: "Raise your shield to reduce incoming damage.",
		},
		{
			name: "cover",
			displayName: "Cover",
			targets: 0,
			icons: "default",
			desc: "Protect a target from harm, sacrificing your defenses."
		},
		{
			name: "ripstance",
			displayName: "Counter Stance",
			targets: 0,
			icons: "default",
			desc: "Enter a countering stance to riposte an attacking foe."
		},
	],

	thief: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "steal",
			displayName: "Steal",
			targets: 0,
			icon: "default",
			desc: "Attempt to steal from a nearby target.",
		},
		{
			name: "poach",
			displayName: "Poach",
			targets: 1,
			icons: "default",
			desc: "Attempt to poach a low-health enemy."
		},
		{
			name: "throwingknife",
			displayName: "Throwing Dagger",
			targets: 0,
			icons: "default",
			desc: "Strongly throw a dagger to deal damage and inflict bleed and reduce attack."
		},
	],

	assassin: [

		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "invis",
			displayName: "Shadowmeld",
			targets: 0,
			icon: "default",
			desc: "Becomes nearly invisible, and hard to detect.",
		},
		{
			name: "poison_blade",
			displayName: "Poison Blade",
			targets: 1,
			icons: "default",
			desc: "Attacks a target with your poisoned knife. Deals double damage while invisible."
		},
		{
			name: "smokebomb",
			displayName: "Smokebomb",
			targets: 0,
			icons: "default",
			desc: "Toss a smokebomb granting temporary invisibility to three allies."
		},
	],
	bard: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "encourage",
			displayName: "War Ballad",
			targets: 0,
			icon: "default",
			desc: "Raise some party members' Att and Acc.",
		},
		{
			name: "charm",
			displayName: "Seductive Charisma",
			targets: 1,
			icons: "default",
			desc: "Attempts to charm an enemy, or reduce charm effects on an ally."
		},
		{
			name: "inspire",
			displayName: "Inspiring Tune",
			targets: 0,
			icons: "default",
			desc: "Increase the accuracy and evasion of three allies."
		},

	],
	cleric: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "blessing",
			displayName: "Blessing of Iron",
			targets: 0,
			icon: "default",
			desc: "Raise some party memebers' defense.",
		},
		{
			name: "cleanse",
			displayName: "Cleanse",
			targets: 1,
			icons: "default",
			desc: "Remove negative effects from a taget."
		},
		{
			name: "holygavel",
			displayName: "Holy Gavel",
			targets: 0,
			icons: "default",
			desc: "Deal damage while reducing three targets' evasion."
		},
	],
	cryomancer: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "chill",
			displayName: "Chilling Mist",
			targets: 0,
			icon: "default",
			desc: "Lowers some foes' attack and evasion.",
		},
		{
			name: "freeze",
			displayName: "Glaciate",
			targets: 1,
			icons: "default",
			desc: "Attempt to freeze a target for multiple turns."
		},
		{
			name: "carapace",
			displayName: "Frozen Carapace",
			targets: 0,
			icons: "default",
			desc: "Surround yourself with frozen briars to retaliate against melee attackers."
		},

	],
	fencer: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "ripstance",
			displayName: "En Garde",
			targets: 0,
			icon: "default",
			desc: "Enter a defensive and ready to parry an attacker.",
		},
		{
			name: "taunt",
			displayName: "Mocking Call",
			targets: 1,
			icons: "default",
			desc: "Attempt to taunt a target into attacking you."
		},
		{
			name: "fanofblades",
			displayName: "Fan of Blades",
			targets: 0,
			icons: "default",
			desc: "Deal moderate damage and reduce evasion for three targets."
		},
	],
	juggernaut: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "warcry",
			displayName: "Battlecry",
			targets: 0,
			icon: "default",
			desc: "Emit a battlecry; Increasing some allies' Att.",
		},
		{
			name: "shatter",
			displayName: "Armor Shatter",
			targets: 1,
			icons: "default",
			desc: "Attack a target, shattering their armor and lowering their Def."
		},
		{
			name: "earthquake",
			displayName: "Quaking Strike",
			targets: 0,
			icons: "default",
			desc: "Strike the ground with your Greathammer, creating a devastating shockwave."
		},
	],
	priest: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "prayer",
			displayName: "Healing Prayer",
			targets: 0,
			icon: "default",
			desc: "Utter a prayer, healing some allies for a small amount.",
		},
		{
			name: "heal",
			displayName: "Divine Touch",
			targets: 1,
			icons: "default",
			desc: "Revive a dead target or massively heal a living target.",
		},
		{
			name: "lightningstorm",
			displayName: "Lightning Storm",
			targets: 0,
			icons: "default",
			desc: "Increase the accuracy and evasion of three allies."
		},
	],
	paladin: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "sealing",
			displayName: "Sealing Strikes",
			targets: 0,
			icon: "default",
			desc: "Enchant your weapon to stun targets that you strike.",
		},
		{
			name: "censure",
			displayName: "Divine Censure",
			targets: 1,
			icons: "default",
			desc: "Censure a target and reduce their scores."
		},
		{
			name: "judgement",
			displayName: "Judgement",
			targets: 0,
			icons: "default",
			desc: "Stun multiple foes with the judgement of God."
		},
	],
	pyromancer: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "pyroclasm",
			displayName: "Searing Steam",
			targets: 0,
			icon: "default",
			desc: "Release a cloud of steam and burn multiple foes.",
		},
		{
			name: "fireball",
			displayName: "Fireball",
			targets: 1,
			icons: "default",
			desc: "Throw a fireball at a target, dealing damage and burning them."
		},
		{
			name: "smokescreen",
			displayName: "Smokescreen",
			targets: 0,
			icons: "default",
			desc: "Create a screen of smoke to reduce the accuracy of three foes."
		},
	],

	sorcerer: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "soulmass",
			displayName: "Conjure Phalanx",
			targets: 0,
			icon: "default",
			desc: "Conjure a retaliatory phalanx to retaliate against attackers.",
		},
		{
			name: "soulspear",
			displayName: "Soulspear",
			targets: 1,
			icons: "default",
			desc: "Conjure a magical spear to attack a foe and deal heavy damage."
		},
		{
			name: "lightwall",
			displayName: "Wall of Solid Light",
			targets: 0,
			icons: "default",
			desc: "Conjure a wall of solid light to deflect magical ranged projectiles."
		},		
	],

	spellblade: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "enchant",
			displayName: "Enchant Armaments",
			targets: 0,
			icon: "default",
			desc: "Enchant your sword and shield, increasing defense.",
		},
		{
			name: "magic_cover",
			displayName: "Magical Protection",
			targets: 1,
			icons: "default",
			desc: "Cover a target, increasing their defenses and granting them a magical phalanx. However your defenses are lowered."
		},
		{
			name: "magic_greatsword",
			displayName: "Conjured Greatsword",
			targets: 0,
			icons: "default",
			desc: "Attack multiple foes with a conjured greatsword."
		},
	],
	swordsman: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "hamstring",
			displayName: "Hamstring",
			targets: 0,
			icon: "default",
			desc: "Create a whirl of your blades, and hamstring multiple foes.",
		},
		{
			name: "slice",
			displayName: "Heavy Slice",
			targets: 1,
			icons: "default",
			desc: "Slice into a target, dealing damage and inflicting bleed."
		},
		{
			name: "flurry",
			displayName: "Blade Flurry",
			targets: 0,
			icons: "default",
			desc: "Unleash a flurry of blades, inflicting minor damage."
		},
	],
	warrior: [
		{
			name: "autoattack",
			displayName: "Basic Attack",
			targets: 0,
			icons: "default",
			desc: "Perform basic attack."
		},
		{
			name: "sharpen",
			displayName: "Grindstone",
			targets: 0,
			icon: "default",
			desc: "Sharpen your axe increasing your attack.",
		},
		{
			name: "armor_break",
			displayName: "Armor Break",
			targets: 1,
			icons: "default",
			desc: "Strike a target, breaking their armor and removing defensive statuses."
		},
		{
			name: "whirlwind",
			displayName: "Whirlwind",
			targets: 0,
			icons: "default",
			desc: "Assault multiple foes, dealing moderate damage and inflicting bleed."
		},
	],

}