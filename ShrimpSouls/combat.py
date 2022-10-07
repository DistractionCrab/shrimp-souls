from dataclasses import dataclasses

class Combat:
	def __init__(self, party, opponents):
		self.__party = {p: (0, 0) for p in party}
		self.__opponents = {p: (0, 0) for p in opponents}

	@property
	def party_dead(self):
		return all(p.dead for p in self.__party)
	
	@property
	def opponents_dead(self):
		return all(p.dead for p in self.__opponents)

	def do_round(self):
		order = list(self.__party.keys()) + list(self.__opponents.keys())
		random.shuffle(order)

		p_fetch = lambda x: self.__party if x in self.__party else self.__opponents
		o_fetch = lambda x: self.__opponents if x in self.__party else self.__party
		actions =  [p.myclass.value.duel_action(p, p_fetch(p), o_fetch(p)) for p in order]

		for a in actions:
			if over(party, opponents):
				break
			a.apply()
