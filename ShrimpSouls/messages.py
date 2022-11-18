from dataclasses import dataclass, field
import json

@dataclass
class RootMessage:
	recv: tuple[str]


@dataclass
class Connected(RootMessage):
	joined: bool = False

	@property
	def json(self):
		return {
			"joined": self.joined
		}

@dataclass
class CharInfo:
	info: object 

	@property
	def json(self):
		return {
			"charsheet": self.info.json
		}

	@property
	def recv(self):
		yield info.name
	
	

@dataclass
class TimeInfo(RootMessage):
	now: int
	length: int

	@property
	def json(self):
		return {
			"tinfo": {
				"now": self.now,
				"ttotal": self.length
			}
		}

@dataclass
class Response(RootMessage):
	msg: tuple[str] = tuple()

	@property
	def json(self):
		return {
			"log": self.msg
		}

@dataclass
class Message(RootMessage):
	msg: tuple[str] = field(default_factory=tuple)
	campinfo: dict = field(default_factory=dict)

	@property
	def json(self):
		return {
			"log": self.msg,
			"campinfo": self.campinfo
		}
	