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
import requests
import persistent
import persistent.mapping
import ShrimpSouls as ss
import ShrimpSouls.campaigns as cps
import ShrimpSouls.messages as messages
import ShrimpSouls.oauth as oauth
import ShrimpSouls.logging as logging
from dataclasses import dataclass


STEP_FREQUENCY = 180
DEACTIVE_TIME = 300
ROUTER_FREQUENCY = 1800


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

class SocketWrapper:
	def __init__(self, ws, parent):
		self.__ws = ws
		self.__parent = parent
		self.__uname = None
		self.__live = True
		self.__dc_reason = None
		self.__uid = None

	@property
	def uname(self):
		return self.__uname

	@property
	def uid(self):
		return self.__uid
	


	async def close(self):
		try:
			await self.__ws.close()
			self.__live = False
		except:
			pass

	async def send(self, msg):
		if not self.__live:
			return
		try:
			if type(msg) is not str:
				msg = json.dumps(msg)
			await self.__ws.send(msg)
		except asyncio.CancelledError:
			self.__dc_reason = "CancelledError: closing socket."
			self.__live = False
		except websockets.exceptions.ConnectionClosedError:
			self.__dc_reason = f"ConnectionClosedError: {self.uid}"
			self.__live = False
		except ConnectionResetError:
			self.__dc_reason = f"ConnectionResetError"
			self.__live = False
		except websockets.exceptions.ConnectionClosedOK:
			self.__live = False
			self.__dc_reason = "Standard disconnection: OK."
		except Exception as ex:
			self.__dc_reason = f"Generic Connection Error: {ex}"
			self.__live = False

	async def recv(self):
		if not self.__live:
			return None
			
		try:
			return await self.__ws.recv()
		except asyncio.CancelledError:
			self.__dc_reason = "CancelledError: closing socket."
			self.__live = False
		except websockets.exceptions.ConnectionClosedError:
			self.__dc_reason = f"ConnectionClosedError: {wsid}"
			self.__live = False
		except ConnectionResetError:
			self.__dc_reason = f"ConnectionResetError"
			self.__live = False
		except websockets.exceptions.ConnectionClosedOK:
			self.__live = False
			self.__dc_reason = "Standard disconnection: OK."
		except Exception as ex:
			self.__dc_reason = f"Generic Connection Error: {ex}"
			self.__live = False

	def __validate_username(self):
		pass

	async def run(self):
		while self.__live:
			try:
				message = await self.recv()
				if message is not None:
					message = json.loads(message)
					if self.__uid is None:
						await self.__connect(message)						
					else:							
						message['socket'] = self
						await self.__parent.message(message)
				else:
					#self.__dc_reason = "No message received on connection."
					await self.close()
			except Exception as ex:
				await self.close()
				self.__dc_reason = f"ERROR in socket: {ex}"


		await self.__parent.message({
			"msg": "disconnect", 
			"socket": self,
			"reason": self.__dc_reason})

	async def __error(self, reason):
		await self.close()
		self.__dc_reason = reason

	async def __connect(self, msg):
		payload = oauth.parse_jwt(msg['jwt'])

		if payload is None:			
			await self.send({
				"error": "Malformed JWT."
			})
			await self.__error("Malformed JWT.")
		else:
			if 'user_id' in payload:
				self.__uid = payload["user_id"]
				r = await oauth.OAUTH.get_username(self.__uid)
				if r is None:
					await self.send({
						"error": ["Could not retrieve username from Twitch."],
						"requestid": True})
				else:
					self.__uname = r["data"][0]["login"]
					logging.log(f"Connected received for c-id {self.__parent.client_id} from {self.__uname}")
					await self.__parent.connect(self)					
			else:
				await self.send(wsid, {"requestid": True})

class Server:
	def __init__(self, game, clientid, db):
		self.__msgs = asyncio.Queue()
		self.__clientid = clientid
		self.__db = db
		self.__last = time.time()
		# Maps from UID to socket	
		self.__idmaps = {}
		# Maps from Uname to socket
		self.__unames = {}
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
	def client_id(self):
		return self.__clientid
	

	@property
	def closed(self):
		return self.__closed
	
	async def __len__(self):
		return len(self.__sockets)

	async def message(self, msg):
		await self.__msgs.put(msg)

	async def server_loop(self):
		while not self.__closed:
			try:
				with self.__db.transaction():
					msg = await self.__msgs.get()
					if msg is Heartbeat:
						await self.__heartbeat()
					else:
						self.__i_time = time.time()
						if msg['msg'] == "connect":
							await self.__connect(msg)
						elif msg['msg'] == 'ability':
							await self.__do_ability(msg)
						elif msg['msg'] == 'item':
							await self.__do_item(msg)
						elif msg['msg'] == 'levelup':
							await self.__level_up(msg)
						elif msg['msg'] == "disconnect":
							await self.__disconnect(msg)					
						elif msg['msg'] == "join":
							await self.__join(msg)
						elif msg['msg'] == "respec":
							await self.__respec(msg)
			except KeyboardInterrupt as ex:
				logging.log(f"Exiting server loop for {self.__clientid}...  (Interrupted)")
				await self.close()
							
		logging.log(f"Exiting main loop for {self.__clientid}")

	async def heartbeat(self):
		try:
			while not self.__closed:
				await self.__msgs.put(Heartbeat)
				await asyncio.sleep(10)
		except KeyboardInterrupt:
			logging.log("Keyboard interrupt on heartbeat.")
		logging.log(f"Exiting heartbeat loop for {self.__clientid}")

	async def __heartbeat(self):
		if len(self.__idmaps) == 0:			
			if time.time() - self.__i_time > DEACTIVE_TIME:
				logging.log(f"Shutting down a server for {self.__clientid}")
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
		s = msg['socket']
		self.__unames.pop(s.uname, None)
		self.__idmaps.pop(s.uid, None)
		r = msg.get('reason', None)

		if s is not None:
			try:
				if s.connected:
					s.close()
			except:
				pass
		logging.log(f"{s.uname} has disconnected. Reason: {r}")

	async def __send_message(self, wsid, m):
		s = self.__sockets[wsid]
		try:
			await s.send(json.dumps(m))
		except:
			pass

	async def __handle_message(self, m):
		for (uname, s) in self.__unames.items():
			if uname in m.recv:
				for ws in s:
					await ws.send(m.json)


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

	async def connect(self, ws):
		

		if ws.uid in self.__idmaps:
			self.__idmap[ws.uid].append(ws)
		else:
			self.__idmaps[ws.uid] = [ws]

		if ws.uname in self.__unames:
			self.__unames[ws.uname].append(ws)
		else:
			self.__unames[ws.uname] = [ws]

		for m in self.__game.connect(ws.uname):
			await self.__handle_message(m)

		await self.__handle_message(
			messages.TimeInfo(
				now=self.__last, 
				length=STEP_FREQUENCY,
				recv=(ws.uname,)))

	async def __level_up(self, msg):
		p = self.__game.get_player(self.__idmaps[msg['wsid']])
		for m in p.level_up(msg['att']):
			await self.__handle_message(m)


	async def __do_ability(self, msg):
		wsid = msg['wsid']
		name = self.__idmaps[wsid]
		for m in self.__game.use_ability(name, msg['ability'], msg['targets']):
			await self.__handle_message(m)

	async def __do_item(self, msg):
		wsid = msg['wsid']
		name = self.__idmaps[wsid]
		for m in self.__game.use_item(name, msg['index'], msg['targets']):
			await self.__handle_message(m)

class Router:
	def __init__(self, test=False):
		self.__test = test
		self.__games = {}
		(self.__dbroot, self.__db) = self.__init_db()

		atexit.register(self.__close)

		if self.__test:
			global STEP_FREQUENCY
			global DEACTIVE_TIME
			global ROUTER_FREQUENCY
			STEP_FREQUENCY = 30
			DEACTIVE_TIME = 30
			ROUTER_FREQUENCY = 30


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

		return (db, cn)
	


	def __get_game(self, i):
		if i in self.__db.root.clients:
			return self.__db.root.clients[i]
		else:
			s = ss.GameManager()
			self.__db.root.clients[i] = s
			return s

	async def __init_server(self, i):
		g = self.__get_game(i)
		s = Server(g, i, self.__dbroot)
		self.__games[i] = s

		asyncio.create_task(s.heartbeat(), name=f"Server({i}) Heartbeat")
		asyncio.create_task(s.server_loop(), name=f"Server({i}) Main Loop")

		return s


	async def __call__(self, ws, path):
		match path.split("/"):
			case ["", ""]: logging.log(f"Root path received from {ws.remote_address}")
			case ["", i]: await self.__route_ws(ws, i)
			case _: logging.log(f"Received unknown route: {path}")

	async def __route_ws(self, ws, i):
		try:
			i = int(i)
			if i in self.__games:
				s = self.__games[i]
			else:
				s = await self.__init_server(i)
			ws = SocketWrapper(ws, s)
			await ws.run()

		except ValueError as ex:
			logging.log(f"Client sent invalid path for connection: {ex}")
			await ws.close()
		except KeyboardInterrupt:
			logging.log(f"Keyboard interrupted socket call.")

	async def main(self):
		looping = True
		while looping:
			#self.__games = {k: v for (k, v) in self.__games.items() if not v.closed}
			transaction.commit()
			await asyncio.sleep(ROUTER_FREQUENCY)

		

async def main(args):
	try:
		if len(args) == 0 or args[0] == 'local':
			m = Router(test=True)
			logging.log("Setting up local insecure server.")
			async with websockets.serve(m, "localhost", 443):
				await m.main()
		elif args[0] == 'networked':
			m = Router()
			logging.log("Setting up networked secure server.")
			root = os.environ['SS_SSL_PATH']
			s = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
			s.load_cert_chain(
				os.path.join(root, "concat.crt"), 
				keyfile=os.path.join(root, "csr.key"))
			async with websockets.serve(m, "0.0.0.0", 443, ssl=s):
				await m.main()
	except asyncio.CancelledError as ex:
		logging.log("Server shutting down: CancelledError")



def run(args):
	asyncio.run(main(args))

