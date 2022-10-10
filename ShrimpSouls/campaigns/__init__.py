import os

HTML = """
	<!DOCTYPE html>
	<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Shrimp Souls Interface</title>
		<style type="text/css">
			body {
				color:  white;
				font-size: 400%;
			}
		</style>
	</head>
	<body>
		<h2>
			No Campaign Active!
		</h2>
	</body>
	</html>
"""

class NullCampaign:
	def __init__(self, players):
		self.__npcs = {}
		self.__players = list(players)	

	@property
	def players(self):
		return self.__players
	
	@property
	def npcs(self):
		return self.__npcs
	

	@npcs.setter
	def npcs(self, v):
		self.__npcs = list(v)

	def step(self):
		print("No campaign active to step.")

	def restore_encounter(self, npcs, statedata, finished):
		self.__npcs = list(npcs)

	def npc_data(self):
		return self._npcs

	def statedata(self):
		return None

	def update_interface(self):
		with open(os.path.join(os.path.split(__file__)[0], "interface.html"), 'w') as out:
			out.write(HTML)
			out.flush()

	@property
	def finished(self):
		return True

	def foe_list(self):
		ftypes = {}
		for n in self.__npcs:
			if not n.dead:
				if type(n) not in ftypes:
					ftypes[type(n)] = []
			
				ftypes[type(n)].append(n)

		lists = [f"{k.__name__}[{', '.join(str(v.npcid) for v in l)}]" for (k, l) in ftypes.items()]

		return ', '.join(lists)

	def get_user(self, name):
		try:
			return next(x for x in self.players if x.name == name)
		except StopIteration:
			raise ValueError(f"No such target as {name}.")

	def get_npc(self, name):
		try:
			return next(x for x in self.__npcs if x.is_named(name))
		except StopIteration:
			raise ValueError(f"No such target as {name}.")

	def get_labeled(self, label):
		try:
			return next(x for x in list(self.__npcs) + list(self.__players) if x.is_named(label))
		except StopIteration:
			raise ValueError(f"No such target as {name}.")
