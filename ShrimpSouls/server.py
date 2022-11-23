import asyncio
import os
import queue
import json
import websockets
import ssl
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


STEP_FREQUENCY = 180

CLIENT_ID = "ec767p01w3r37lrj9gfvcz9248ju9v"
with open(os.path.join(os.environ["SS_SSL_PATH"], "APP_SECRET.json"), 'r') as read:
	SECRETS = json.loads(read.read())


def server_secret():
	return SECRETS["server_secret"]

def jwt_secret():
	return base64.b64decode(SECRETS["jwt_secret"])

def parse_jwt(msg):
	s = jwt_secret()
	try:
		return jwt.decode(msg['token'], jwt_secret(), algorithms=["HS256"])
	except:
		return None



async def get_username(i):
	try:
		async with aiohttp.ClientSession() as session:
			url = f'https://api.twitch.tv/helix/users?id={i}'
			headers = {
				"Authorization": "Bearer " + SECRETS['oauth_token'],
				"Client-ID": CLIENT_ID,
			}
			r = await session.get(url, headers=headers)
			return json.loads(await r.text())
	except:
		return None



# Basic marker class used to keep the server flowing.
class Heartbeat:
	pass

class CloseServer:
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
	def __init__(self, game, clientid):
		self.__msgs = asyncio.Queue()
		self.__clientid = clientid
		self.__sockets = {}
		self.__connections = {}
		self.__last = time.time()		
		self.__idmaps = {}
		self.__unames = {}
		self.__wsid_ct = 0
		self.__game = game
		self.__closed = False
		self.__i_time = time.time()

	async def close(self):
		self.__closed = True

		for s in self.__sockets.values():
			try:
				s.close()
			except:
				pass

	@property
	def closed(self):
		return self.__closed
	
	async def __len__(self):
		return len(self.__sockets)


	async def server_loop(self):
		while not self.__closed:
			try:
				msg = await self.__msgs.get()
				if msg is Heartbeat:
					await self.__heartbeat()
				else:
					self.__i_time = time.time()
					if msg['msg'] == "connect":
						await self.__connect(msg)
					elif msg['msg'] == 'ability':
						await self.__do_ability(msg)
					elif msg['msg'] == 'levelup':
						await self.__level_up(msg)
					elif msg['msg'] == "disconnect":
						await self.__disconnect(msg)					
					elif msg['msg'] == "join":
						await self.__join(msg)
					elif msg['msg'] == "respec":
						await self.__respec(msg)
			except KeyboardInterrupt as ex:
				print("Exiting server loop...  (Interrupted)")
				self.close()
							
		print(f"Exiting main loop for {self.__clientid}")

	async def heartbeat(self):
		while not self.__closed:
			await self.__msgs.put(Heartbeat)
			await asyncio.sleep(10)
		print(f"Exiting heartbeat loop for {self.__clientid}")

	async def __heartbeat(self):
		if len(self.__sockets) == 0:			
			if time.time() - self.__i_time > 300:
				print(f"Shutting down a server for {self.__clientid}")
				await self.close()
		else:
			self.__i_time = time.time()
			now = time.time()
			if now - self.__last >= STEP_FREQUENCY:

				self.__last = now
				for m in self.__game.step():
					await self.__handle_message(m)


				await self.__handle_message(
						messages.TimeInfo(
							now=self.__last, 
							length=STEP_FREQUENCY,
							recv=tuple(self.__game.players)))


	async def __disconnect(self, msg):
		i = msg['wsid']
		print(f"Disconnecting socket for conn {i} and uname {self.__idmaps[i]}")
		s = self.__sockets.pop(i, None)
		self.__unames.pop(self.__idmaps.get(i), None)
		self.__idmaps.pop(i, None)

		if s is not None:
			try:
				if s.connected:
					s.close()
			except:
				pass

	async def __send_message(self, wsid, m):
		s = self.__sockets[wsid]
		try:
			await s.send(json.dumps(m))
		except:
			pass

	async def __handle_message(self, m):
		for n in m.recv:
			if n in self.__unames:
				t = m.json
				await self.__sockets[self.__unames[n]].send(json.dumps(t))


	async def __join(self, msg):
		name = self.__idmaps[msg['wsid']]
		
		for m in self.__game.join(name):
			await self.__handle_message(m)


	async def __respec(self, msg):
		wsid = msg['wsid']
		cl = msg['data']
		p = self.__game.get_player(self.__idmaps[wsid])

		for m in self.__game.respec(p, cl):
			await self.__handle_message(m)

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
					await self.__send_message(wsid, {
						"error": ["Could not retrieve username from Twitch."],
						"requestid": True})
				else:
					uname = r["data"][0]["login"]
					self.__idmaps[wsid] = uname
					self.__unames[uname] = wsid
					print(f"Connected received for c-id {self.__clientid} from {uname}")
					for m in self.__game.connect(uname):
						await self.__handle_message(m)
					await self.__handle_message(
						messages.TimeInfo(
							now=self.__last, 
							length=STEP_FREQUENCY,
							recv=(uname,)))
						
			else:
				await self.__send_message(wsid, {"requestid": True})



	async def __level_up(self, msg):
		p = self.__game.get_player(self.__idmaps[msg['wsid']])
		for m in p.level_up(msg['att']):
			await self.__handle_message(m)


	async def __do_ability(self, msg):
		wsid = msg['wsid']
		name = self.__idmaps[wsid]
		for m in self.__game.use_ability(name, msg['ability'], msg['targets']):
			await self.__handle_message(m)


	async def __call__(self, ws):
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
			except websockets.exceptions.ConnectionClosedError:
				print(f"Connection closed: {wsid}")
				reading = False
			except ConnectionResetError:
				print(f"Connection closed: {wsid}")
				reading = False
			except websockets.exceptions.ConnectionClosedOK:
				print(f"Connection closed {wsid}")
				reading = False
			except ValueError as ex:
				print(f"Client sent invalid path for connection: {ex}")
				reading = False
			except Exception as ex:
				print(f"Generic Connection Error: {ex}")
				reading = False


		await self.__msgs.put({"msg": "disconnect", "wsid": wsid})

class Router:
	def __init__(self, test=False):
		self.__test = test
		self.__games = {}
		self.__db = self.__init_db()

		atexit.register(self.__close)

		if self.__test:
			global STEP_FREQUENCY
			STEP_FREQUENCY = 30


	def __close(self):
		transaction.commit()
		self.__db.close()

	def __init_db(self):
		if self.__test:
			DB_PATH = os.path.join(os.path.split(__file__)[0], "../../databases/testing.fs")
			db = ZODB.DB(DB_PATH)
			cn = db.open()
		else:
			DB_PATH = os.path.join(os.environ["SS_DB_PATH"], "ss_db.fs")
			db = ZODB.DB(DB_PATH)
			cn = db.open()

		if "clients" not in cn.root():
			cn.root.clients = persistent.mapping.PersistentMapping()

		return cn
	


	def __get_game(self, i):
		if i in self.__db.root.clients:
			return self.__db.root.clients[i]
		else:
			s = ss.GameManager()
			self.__db.root.clients[i] = s
			return s

	async def __call__(self, ws, path):
		try:
			i = int(path[1:])

			if i not in self.__games:
				g = self.__get_game(i)
				s = Server(g, i)
				self.__games[i] = s

				asyncio.create_task(s.heartbeat(), name=f"Server({i}) Heartbeat")
				asyncio.create_task(s.server_loop(), name=f"Server({i}) Main Loop")			
			else:
				s = self.__games[i]

			
			await s(ws)

		except asyncio.CancelledError:
			print("Program Exited closing socket.")
		except websockets.exceptions.ConnectionClosedError:
			print(f"Connection closed: {wsid}")
		except ConnectionResetError:
			print(f"Connection closed: {wsid}")
		except websockets.exceptions.ConnectionClosedOK:
			print(f"Connection closed {wsid}")
		except ValueError as ex:
			print(f"Client sent invalid path for connection: {ex}")
			await ws.close()
		except Exception as ex:
			print(f"Generic Connection Error: {ex}")

	async def main(self):
		looping = True
		while looping:
			self.__games = {k: v for (k, v) in self.__games.items() if not v.closed}
			await asyncio.sleep(100)

		

async def main(args):
	if len(args) == 0 or args[0] == 'local':
		m = Router(test=True)
		print("Setting up local insecure server.")
		async with websockets.serve(m, "localhost", 443):
			await m.main()
	elif args[0] == 'networked':
		m = Router()
		print("Setting up networked secure server.")
		root = os.environ['SS_SSL_PATH']
		s = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
		s.load_cert_chain(
			os.path.join(root, "concat.crt"), 
			keyfile=os.path.join(root, "csr.key"))
		async with websockets.serve(m, "0.0.0.0", 443, ssl=s):
			await m.main()

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

