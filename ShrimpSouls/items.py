from dataclasses import dataclass
import random

@dataclass
def BaseItem:
	name: str
	charges: int


	def __hash__(self):
		return hash(self.name)


@dataclass
class HealthPotionMinor(BaseItem):
	name: str = "Minor Health Potion"
	charges: int = 1

	def use(self, p):
		if self.charges > 0:			
			amt = random.randint(1, 6)
			p.damage(-amt)

			return f"{p.label} used {str(self)} to heal for {amt} health."
		else:
			return f"No charges of {self.name} to be used."

	def __str__(self):
		return f"Minor Health Potion ({self.charges})"


def from_string(s):
	return eval(s)