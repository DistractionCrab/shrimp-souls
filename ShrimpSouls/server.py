import asyncio
import os
import queue
import json
import websockets
import ssl
import requests
import aiohttp
import time
import enum
import jwt
import base64
import ZODB
import transaction
import atexit
import persistent
import persistent.mapping
import ShrimpSouls as ss
import ShrimpSouls.campaigns as cps
import ShrimpSouls.messages as messages
from dataclasses import dataclass

OAUTH_PATH = os.path.join(os.path.split(__file__)[0], "oauth.txt")
DB_PATH = os.path.join(os.path.split(__file__)[0], "../databases/testing.fs")
with open(OAUTH_PATH, 'r') as inp:
	OAUTH_DATA = json.loads(inp.read())
CLIENT_ID = "ec767p01w3r37lrj9gfvcz9248ju9v"

def server_secret():
	return "j5mcv9re65gp62xihqxqyk402laf81"

def jwt_secret():
	return base64.b64decode("6JvuBgcH+U2M/upQ7fwf+X9rj48BV7nyYvx5H6H1+9g=")

def parse_jwt(msg):
	s = jwt_secret()
	try:
		return jwt.decode(msg['token'], jwt_secret(), algorithms=["HS256"])
	except:
		return None

def get_db_conn(testing=False):
	if testing:
		db = ZODB.DB(DB_PATH)
		return db.open()
	else:
		db = ZODB.DB(DB_PATH)
		return db.open()

def init_db(testing=False):
	cn = get_db_conn(testing=testing)

	if "clients" not in cn.root():
		cn.root.clients = persistent.mapping.PersistentMapping()

	#transaction.commit()

	return cn

DATABASE = init_db(testing=True)

def close_server():
	transaction.commit()
	DATABASE.close()
atexit.register(close_server)

async def get_username(i):
	try:
		async with aiohttp.ClientSession() as session:
			url = f'https://api.twitch.tv/helix/users?id={i}'
			headers = {
				"Authorization": "Bearer " + OAUTH_DATA['access_token'],
				"Client-ID": CLIENT_ID,
			}
			r = await session.get(url, headers=headers)
			return json.loads(await r.text())
	except:
		return None



# Basic marker class used to keep the server flowing.
class Heartbeat:
	pass



class Messages(enum.Enum):
	CONNECTONLY = (lambda g, p: {
			'charsheet': p.json,
			"joined": g.is_joined(p)
		})
	UPDATE = (lambda g, msg, p: {
			"log": msg,
			"joined": g.is_joined(p),
			"charsheet": p.json,
			"partyinfo": [p.json for p in g.party],
			"npcinfo": [p.json for p in g.npcs],
		})
	ERROR = (lambda msg: {"msg": "error", "data": f"ERROR: {msg}"})



class Server:
	def __init__(self, clientid, test=False):
		self.__clientid = clientid		
		self.__msgs = asyncio.Queue()
		self.__sockets = {}
		self.__connections = {}
		self.__last = time.time()		
		self.__idmaps = {}
		self.__test = test
		self.__wsid_ct = 0


		if clientid not in DATABASE.root.clients:
			 self.__db.clients[clientid] = ss.GameManager()

		self.__game = DATABASE.root.clients[clientid]


	async def server_loop(self):
		while True:
			v = await self.__msgs.get()
			await self.__handle_msg(v)

	async def heartbeat(self):
		while True:
			await self.__msgs.put(Heartbeat())
			await asyncio.sleep(10)

	def player_to_json(p):
		if isinstance(p, str):
			p = self.__game.get_player(p)
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
		if isinstance(p, str):
			p = self.__game.get_npc(p)
		return {
			'name': p.name,
			'hp': p.hp,
			'max_hp': p.max_hp,
			'xp': p.xp,
			'status': p.status.__dict__
		}

	async def __send_message(self, wsid, m):
		s = await self.__get_sock(wsid)
		try:
			await s.send(json.dumps(m))
		except:
			pass

	async def __get_uname(self, wsid):
		return self.__idmaps[wsid]

	async def __join(self, msg):
		try:
			name = self.__idmaps[msg['wsid']]
			self.__game.join(name)
			await self.__handle_update(
				messages.Message(msg=[f"{name} has joined the party!"], 
				users=self.__game.party,
				npcs=self.__game.npcs))
		except Exception as ex:
			await self.__send_message(msg['wsid'], {"log": f"Error on joining: {ex}"})


	async def __respec(self, msg):
		wsid = msg['wsid']
		cl = msg['data']
		p = self.__game.get_player(self.__idmaps[wsid])
		m = self.__game.respec(p, cl)

		if m.is_err:
			await self.__send_message(wsid, {"log": m.msg[-1]})
		else:			
			await self.__handle_update(m)


	async def __connect(self, msg):
		wsid = msg['wsid']
		self.__sockets[wsid] = msg["socket"]
		payload = parse_jwt(msg['jwt'])

		if payload is None:
			await self.__send_message(wsid, {"error": "Malformed JWT."})
		else:
			if 'user_id' in payload:
				r = await get_username(payload['user_id'])
				if r is None:
					await self.__send_message(wsid, {"error": "Could not retrieve username from Twitch."})
				else:
					uname = r["data"][0]["login"]
					self.__idmaps[wsid] = uname
					player = self.__game.get_player(uname)
					if self.__game.is_joined(uname):
						await self.__send_message(wsid, Messages.UPDATE(self.__game, ["Connected"], player))						
					else:
						await self.__send_message(wsid, Messages.CONNECTONLY(self.__game, player))
						
			else:
				await self.__send_message(wsid, Messages.ERROR("User ID not supplied."))


	async def __level_up(self, msg):
		p = self.__game.get_player(self.__idmaps[msg['wsid']])
		m = p.level_up(msg['att'])

		if m.is_err:
			await self.__send_message(msg['wsid'], {
					"log": [m.msg]
				})
		else:
			await self.__send_message(msg['wsid'], {
					"charsheet": p.json,
					"log": [m.msg]
				})
			
	async def __handle_update(self, msg):
		items = list(self.__idmaps.items())
		for (wsid, r) in items:
			p = self.__game.get_player(r)
			send = {
				'log': msg.msg,
				'charsheet': p.json,
				'partyinfo': [u.json for u in msg.users],
				'npcinfo': [u.json for u in msg.npcs],
				'refreshEntities': msg.refreshEntities,
				"joined": self.__game.is_joined(p)
			}
			await self.__send_message(wsid, send)


	async def __do_ability(self, msg):
		wsid = msg['wsid']
		name = self.__idmaps[wsid]
		msg = self.__game.use_ability(name, msg['ability'], msg['targets'])
		if msg.is_err:
			await self.__send_message(wsid, {"log": msg.msg})
		else:
			await self.__handle_update(msg)


	async def __handle_msg(self, msg):
		if isinstance(msg, Heartbeat):
			now = time.time()
			if now - self.__last >= 180:
				self.__last = now
				msg = self.__game.step()

				await self.__handle_update(msg)

		else:
			if msg['msg'] == "connect":
				await self.__connect(msg)
			elif msg['msg'] == 'ability':
				await self.__do_ability(msg)
			elif msg['msg'] == 'levelup':
				await self.__level_up(msg)
			elif msg['msg'] == "disconnect":
				del self.__sockets[msg["wsid"]]
				del self.__idmaps[msg["wsid"]]
			elif msg['msg'] == "join":
				await self.__join(msg)
			elif msg['msg'] == "respec":
				await self.__respec(msg)


	async def __add_sock(self, ws):
		index = 0 if len(self.__sockets) == 0 else max(self.__sockets.keys()) + 1
		self.__sockets[index] = ws

		return index

	async def __get_sock(self, wsid):
		if wsid in self.__sockets:
			return self.__sockets[wsid]
		else:
			return None

	async def __call__(self, ws):
		#wsid = await self.__add_sock(ws)
		wsid = self.__wsid_ct
		self.__wsid_ct += 1
		reading = True
		while reading:
			try:
				message = await ws.recv()
				message = json.loads(message)
				message['wsid'] = wsid
				message['socket'] = ws
				await self.__msgs.put(message)
			except asyncio.CancelledError:
				print("Program Exited closing socket.")
				reading = False
			except websockets.exceptions.ConnectionClosedOK:
				print(f"Connection closed.")
				reading = False



		await self.__msgs.put({"msg": "disconnect", "wsid": wsid})

class Router:
	def __init__(self, test=False):
		self.__test = test
		self.__games = {}

	async def __call__(self, ws, path):
		try:
			i = int(path[1:])
			print(f"Received Connection for channelId {i}")

			if i not in self.__games:
				s = Server(i, test=self.__test)
				self.__games[i] = s
				
			else:
				s = self.__games[i]

			asyncio.create_task(s.heartbeat(), name=f"Server({i}) Heartbeat")
			asyncio.create_task(s.server_loop(), name=f"Server({i}) Main Loop")
			await s(ws)

		except asyncio.CancelledError:
			print("Program Exited closing socket.")
		except websockets.exceptions.ConnectionClosedOK:
			print(f"Connection closed.")
		except ValueError as ex:
			print(f"Client sent invalid path for connection: {ex}")
			await ws.close()
			raise ex

	async def main(self):
		looping = True
		while looping:
			await asyncio.sleep(300)

		

async def main(args):
	if len(args) == 0 or args[0] == 'local':
		m = Router(test=True)
		print("Setting up local insecure server.")
		async with websockets.serve(m, "localhost", 443):
			await m.main()
			pass
			#await asyncio.gather(m.heartbeat(), m.server_loop())
	elif args[0] == 'networked':
		m = Router()
		print("Setting up networked secure server.")
		s = ssl.create_default_context()
		async with websockets.serve(m, "0.0.0.0", 443, ssl=s):
			await m.main()
			#await asyncio.gather(m.heartbeat(), m.server_loop())

def update_ip():

	username = input("Username: ")
	password = input("Password: ")
	ip = "82.180.173.104"
	subdomain = "shrimpsouls.distractioncrab.net"
	URL = f"https://{username}:{password}@domains.google.com/nic/update?hostname={subdomain}&myip={ip}"

	r = requests.post(URL)

	print(r)

def run(args):
	asyncio.run(main(args))

