import asyncio
import os
import queue
import json
import websockets
import ssl
import requests
import time
import enum
import ShrimpSouls as ss

OAUTH_PATH = os.path.join(os.path.split(__file__)[0], "oauth.txt")
with open(OAUTH_PATH, 'r') as inp:
	OAUTH_DATA = json.loads(inp.read())
CLIENT_ID = "ec767p01w3r37lrj9gfvcz9248ju9v"

def server_secret():
	return "j5mcv9re65gp62xihqxqyk402laf81"

def get_username(id):
	r = requests.get(
		f'https://api.twitch.tv/helix/users?id={id}',
		headers={
			"Authorization": "Bearer " + OAUTH_DATA['access_token'],
			"Client-ID": CLIENT_ID,
		}
	)
	return r

# Basic marker class used to keep the server flowing.
class Heartbeat:
	pass



def player_to_json(p):
	if isinstance(p, str):
		p = ss.get_player(p)
	return {
		'name': p.name,
		'hp': p.hp,
		'max_hp': p.max_hp,
		'xp': p.xp,
		'xp_req': p.get_xp_req(),
		'class': p.myclass.cl_string,
		'attributes': p.attributes.__dict__,
		'status': p.status.__dict__
	}

def enemy_to_json(p):
	return {
		'name': p.name,
		'hp': p.hp,
		'max_hp': p.max_hp,
		'xp': p.xp,
		'status': p.status.__dict__
	}

class Messages(enum.Enum):
	JOIN = (lambda p: json.dumps({
			'msg': "charsheet",
			'data': {
				'name': p.name,
				'hp': p.hp,
				'max_hp': p.max_hp,
				'xp': p.xp,
				'xp_req': p.get_xp_req(),
				'class': p.myclass.cl_string,
				'attributes': p.attributes.__dict__,
				'status': p.status.__dict__
			}
		}))
	STEP = (lambda m: json.dumps({
			'msg': "printout",
			'data': str(m)
		}))
	PLAYERS = (lambda g: json.dumps({
			"msg": "partyinfo", 
			"data": [player_to_json(p) for p in g.players]
		}))



class Server:
	def __init__(self):
		self.__msgs = asyncio.Queue()
		self.__lock = asyncio.Lock()
		self.__sockets = {}
		self.__connections = {}
		self.__last = time.time()
		self.__game = ss.GameManager()
		self.__idmaps = {}


	def get_message(self):
		return self.__msgs.get()


	async def parse_msg(self, msg):
		if msg['msg'] == "join":
			wsid = msg['wsid']
			i = msg['userid']
			r = get_username(msg['userid'])
			if r.status_code == 200:
				r = json.loads(r.text)
				uname = r["data"][0]["login"]
				responses = [
					Messages.JOIN(ss.get_player(uname, init=True)),
					Messages.PLAYERS(self.__game)
				]
				self.__idmaps[wsid] = uname
			else:
				responses = []

			return responses
		elif msg['msg'] == 'basicclassaction':
			wsid = msg['wsid']
			async with self.__lock:
				name = self.__idmaps[wsid]
			msg = self.__game.action(name)
			await self.__handle_update(msg)
			return []
		else:
			return [];

	async def server_loop(self):
		while True:
			v = await self.__msgs.get()
			await self.__handle_msg(v)

	async def __handle_update(self, msg):	
		async with self.__lock:
			party = [player_to_json(r) for r in self.__game.players]
			players = [player_to_json(r) for r in self.__idmaps.values()]
			for (wsid, r) in self.__idmaps.items():
				msg = {
					'msg': "update",
					'data': msg,
					'player': player_to_json(r),
					'party': party
				}
				await self.__sockets[wsid].send(json.dumps(msg))
			


	async def __handle_msg(self, msg):
		if isinstance(msg, Heartbeat):
			now = time.time()
			if now - self.__last >= 30:
				self.__last = now
				await self.__handle_update(self.__game.step())

		else:
			responses = await self.parse_msg(msg)
			ws = await self.__get_sock(msg["wsid"])
			for r in responses:	
				#print(f"r = {r}")			
				await ws.send(r)				
				

	async def heartbeat(self):
		while True:
			await self.__msgs.put(Heartbeat())
			await asyncio.sleep(10)

	async def __broadcast(self, msg):
		async with self.__lock:
			rem = []
			for i, ws in self.__sockets.items():
				try:
					await ws.send(msg)
				except:
					rem.append(i)

			for i in rem:
				del self.__sockets[i]

	async def __add_sock(self, ws):
		async with self.__lock:

			index = 0 if len(self.__sockets) == 0 else max(self.__sockets.keys()) + 1
			self.__sockets[index] = ws

			return index

	async def __get_sock(self, wsid):
		async with self.__lock:
			if wsid in self.__sockets:
				return self.__sockets[wsid]
			else:
				return None

	async def __call__(self, ws, path):
		wsid = await self.__add_sock(ws)
		print("Received connection.")
		reading = True
		while reading:
			try:
				#message = await asyncio.wait_for(websocket.recv(), timeout)
				message = json.loads(await ws.recv())
				message['wsid'] = wsid
				await self.__msgs.put(message)
			except asyncio.CancelledError:
				print("Program Exited closing socket.")

				reading = False
			except websockets.exceptions.ConnectionClosedOK:
				print(f"Connection closed.")
				#ws.close()
				reading = False

		async with self.__lock:
			del self.__sockets[wsid]
			del self.__idmaps[wsid]


async def main():
	m = Server()

	#async with websockets.serve(handle_thing, "", 8001):
	s = ssl.create_default_context()
	#async with websockets.serve(m, "", 443, ssl=s):
	async with websockets.serve(m, "", 443):
		#await asyncio.Future()

		#await m.handler_loop()  # run forever
		#await m.server_loop()
		await asyncio.gather(m.heartbeat(), m.server_loop())



def run():
	asyncio.run(main())
