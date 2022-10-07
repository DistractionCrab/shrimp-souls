import ShrimpSouls as ss
import random

DICE_OUTCOMES = {
	1: [
		"They have suffered a horrible fate.",
		"Their seduction attempt against the dragon has failed.",
		"They stub their toe, slip on some ice while jumping in pain, fall down into a pit, and wake a cave troll.",
		"They step on a sleeping Cactuar, and the cactuar uses 1000 needles.",
		"Their number is not a prime number; Also they fall down a hole with spikes.",
		"YOUDIED",
		"They've been banished to the meatloaf dimension, but all the meatloaf is gone."
	],
	2: [
		"They attempt to butter a muffin, but lose a pinky in the process.",
		"A pack of roving goblins steals their sushi.",
		"They a find a genie of the muffin, but is free thanks to Noob_almost, and will no longer grant you wishes.",
		"Their number is a prime number.",
	],
	3: [
		"They go to pet a cat, but the cat mauls them out of spite.",
		"They find a cursed dagger that can only heal those it stabs.",
		"Their number is a prime number.",
		"They are cursed with unending flatulence.",
	],
	4: [
		"Their bowl of ramen ends up burning their mouth.",
		"Their number is not a prime number.",
		"A seagull bombards them through their window.",
	],
	5: [
		"They stub their toe as they go to pet a cat.",
		"They save a turtle, that turns out to be evil and curses them.",
		"Their number is a prime number.",
		"They get a free pizza, but it has their least favourite toppings.",
	],
	6: [
		"They dropped their book in the water.",
		"Their ramen is missing some spice, and is barely adequate.",
		"Their number is not a prime number.",
	],
	7: [
		"They go to pet a puppy, but tripped and end up bopping it on the nose.",
		"They meet a stranger, and this stranger steals their shrimp.",
		"Their number is a prime number.",
		"They receive their favourite beer, but it's flat and warm.",
	],
	8: [
		"Their next soup will be perpetually cold.",
		"They find a soft puppy, but the puppy runs away before they can pet it.",
		"Their number is not a prime number, but is a perfect cube.",
		"A bumblebee flies bombards into them, knocking them over, but they find a somewhat shiny coin.",
	],
	9: [
		"Their next sushi roll will not have enough spicy mayo.",
		"They find a rusted coin.",
		"Their number is not a prime number, but is a perfect square.",
	],
	10: [
		"An uncomfortable smell graces their nose.",
		"Their shiny rock falls into the river, and is stolen by a fish.",
		"Their number is not a prime number.",
	],
	11: [
		"A comfortable breeze blows by.",
		"They find a shiny rock by the river.",
		"Their number is a prime number.",
	],
	12: [
		"They find a shiny coin.",
		"Their next sushi has adequate spicy mayo and diced crab.",
		"Their number is not a prime number.",
	],

	13: [
		"They find a soft puppy, and pet it.",
		"Their next soup will be warm for as long as they need.",
		"Their number is a prime number.",
	],
	14: [
		"They greet a stranger, and receive a free fish.",
		"They go to pet a puppy, and the puppy licks them.",
		"Their number is not a prime number.",
	],
	15: [
		"The ramen they ordered was perfectly hot and spicy.",
		"Their book falls, but they managed to catch it before it lands in the water.",
		"Their number is not a prime number.",
	],
	16: [
		"They save a turtle, and it grants them ten gold coins.",
		"They successfully pet a cat without incident.",
		"Their number is not a prime number, is a perfect 4-dimensional cube.",
	],
	17: [
		"Their number is a prime number.",
		"Their ramen is the perfect temperature.",
	],
	18: [
		"They discover a magical dagger, that is not cursed, and can be used to stab.",
		"They go to pet a cat, and it sits in their lap and purrs.",
		"Their number is not a prime number.",
	],

	19: [
		"They convince a pack of roving goblins to give them their sushi.",
		"They successfully butter a muffin, that happens to be the home of a genie.",
		"Their number is a prime number.",
	],

	20: [
		"They have successfully seduced the dragon.",
		"They have found the well of infinite ramen.",
		"An anvil narrowly misses falling on them, they find 50 gold coins in the hole made by the anvil, and a goat gifts them a watermelon.",
		"They stumble across their favourite shiny Pokemon",
		"Their number is not a prime number, but are able to solve the Riemann Hypothesis.",
		"They've been banished to the meatloaf dimension, and there's plenty of meatloaf."
	],
}

DICE_SCORES = {
	1: -10,
	2: 2,
	3: 3,
	4: 4,
	5: 5,
	6: 6,
	7: 7,
	8: 8,
	9: 9,
	10: 10,
	11: 11,
	12: 12,
	13: 13,
	14: 14,
	15: 15,
	16: 16,
	17: 17,
	18: 18,
	19: 19,
	20: 20

}

def roll_dice(name):
	roll = int(ss.roll_dice()[0])
	user = ss.User(name)
	msg = ''

	amt = 0
	if roll == 1:
		user.bonk()

	v = DICE_SCORES[roll]
	if v >=0:
		v += user.luck
	amt = user.add_shrimp(v)


	outcome = random.choice(DICE_OUTCOMES[roll])
	msg += f"{name} has rolled a {roll}. {outcome} (shrimp={amt}). "

	if roll == 20:
		msg += f"{name} got lucky and can roll again..."
		print(msg)
		roll_dice(name)
	else:
		print(msg)

	
