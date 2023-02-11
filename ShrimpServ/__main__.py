import websockets
import asyncio
import json
import ShrimpServ.logging as logging
import ShrimpServ.oauth as oauth

class Player:
	def __init__(self, ws, host):
		self.__ws = ws
		self.__host = host
		self.__uname = self.__get_uname()
		raise ValueError("Could not retrieve username")

	async def __get_uname(self):
		try:
			msg = await self.__ws.recv()
			payload = oauth.parse_jwt(msg)

			if payload is None:
				self.__ws.send({
					"log": "Invalid JWT"
				})
				self.close()
			else:
				i = payload["user_id"]
				n = oauth.OAUTH.get_username(i)
				if n is None:
					self.__ws.send({
						"log": "Could not retrieve username from Twitch."
					})
					self.close()
				else:
					msg["uname"] = n
					self.__host.send(msg)
					return n

		except:
			self.__close()


	async def main(self):
		while True:
			try:
				msg = self.__ws.recv()
				self.__host.send(msg)
			except ex:
				logging.log(f"Connection terminated for {self.__uname}: {ex}")


	async def send(self, msg):
		try:
			if isinstance(msg, str):
				self.__ws.send(msg)
			else:
				self.__ws.send(json.dumps(msg))
		except:
			pass

	async def close(self):
		self.__host.remove_player(self)
		try:
			await self.__ws.close()
		except:
			pass

class Host:
	def __init__(self, ws):
		self.__ws = ws
		self.__players = []

	def __delitem__(self, player):
		pass

	async def add_player(ws):
		try:
			p = Player(ws, self)
			self.__players.append(p)
			return p
		except:
			return None

	async def remove_player(self, p):
		try:
			self.__players.remove(p)
		except:
			pass

	async def close(self):
		try:
			await self.__ws.close()
		except:
			pass

		for p in self.__players:
			await p.close()


class Router:
	def __init__(self):
		self.__hosts = {}

	async def main(self):
		while True:
			await asyncio.sleep(500)

	async def __call__(self, ws, path):
		print("taco")
		match path.split("/"):
			case ["player", i]: self.__connect_player(ws, i)
			case ["host", i]: print(f"Connecting host {i}")
			case _: logging.log(f"Received unknown route: {path}")

	async def __connect_host(self, ws, host):
		if host in self.__hosts:
			h = self.__hosts[host]
			h.close()
			self.__hosts[host] = Host(ws)

	async def __connect_player(self, ws, host):
		if host in self.__hosts:
			p = await self.__hosts[host].add_player(ws)
			if p is not None:
				await p.main()
		else:
			await ws.send(json.dumps({
				"log": "Streamer has not opened up the game."
			}))
			ws.close()

	async def remove_host(self, h):
		pass

async def main(args):
	try:
		if len(args) == 0 or args[0] == 'local':
			m = Router()
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


import sys
asyncio.run(main(sys.argv[1:]))