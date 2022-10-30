from dataclasses import dataclass, field


@dataclass
class Message:
	msg: list[str] = field(default_factory=list)
	users: list = field(default_factory=list)
	npcs: list = field(default_factory=list)
	refreshEntities: bool = False

	@property
	def is_err(self):
		return False

	def __getitem__(self, i):
		return self.msg[i]


@dataclass
class Error(Message):
	@property
	def is_err(self):
		return True
	