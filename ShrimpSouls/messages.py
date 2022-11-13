from dataclasses import dataclass, field



class EmptyMessage:
	@property
	def is_empty(self):
		return True
	

	@property
	def is_err(self):
		return False

	@property
	def is_response(self):
		return False
	

	def __getitem__(self, i):
		return None

EMPTY = EmptyMessage()

@dataclass
class Response:
	msg: list[str] = field(default_factory=list)

	@property
	def is_err(self):
		return False

	@property
	def is_response(self):
		return True
	

	def __getitem__(self, i):
		return self.msg[i]

	@property
	def is_empty(self):
		return False



@dataclass
class Message:
	msg: list[str] = field(default_factory=list)
	users: list = field(default_factory=list)
	npcs: list = field(default_factory=list)
	remove_player: list = field(default_factory=list)
	remove_npc: list = field(default_factory=list)
	refreshEntities: bool = False

	@property
	def is_err(self):
		return False

	def __getitem__(self, i):
		return self.msg[i]

	@property
	def is_response(self):
		return False

	@property
	def is_empty(self):
		return False


@dataclass
class Error:
	@property
	def is_err(self):
		return True

	@property
	def is_response(self):
		return False

	@property
	def is_empty(self):
		return False
	