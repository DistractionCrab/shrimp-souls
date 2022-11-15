from dataclasses import dataclass, field
import json



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
	msg: tuple[str] = field(default_factory=tuple)
	campinfo: dict = field(default_factory=dict)

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
	msg: tuple[str] = field(default_factory=tuple)
	recv: tuple[str] = field(default_factory=tuple)
	users: tuple = field(default_factory=tuple)
	npcs: tuple = field(default_factory=tuple)
	remove_player: tuple = field(default_factory=tuple)
	remove_npc: tuple = field(default_factory=tuple)
	refreshEntities: bool = False
	campinfo: dict = field(default_factory=dict)

	@property
	def json(self):
		return {
			"log": self.msg,
			"campinfo": self.campinfo
		}
	

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
	msg: tuple[str] = field(default_factory=tuple)
	
	@property
	def is_err(self):
		return True

	@property
	def is_response(self):
		return False

	@property
	def is_empty(self):
		return False
	