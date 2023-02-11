import eel
import os
import ZODB
import ShrimpSouls as ss

APP_DIR = os.environ["APPDATA"]
DB_PATH = os.path.join(APP_DIR, "shrimpsouls.fs")



class Server:
	def __init__(self):
		self.__db = ZODB.DB(DB_PATH)
		self.__last = time.time()
		# Maps from UID to socket	
		self.__game = game
		self.__closed = False
		self.__i_time = time.time()
	
	def __init_db(self):
		db = ZODB.DB(DB_PATH)

		if "game" not in db.root():
			db.root["game"] = ss.GameManager()

		return db

	def message(self, msg):
		self.__msgs.put(msg)

	def server_loop(self):
		while not self.__closed:
			try:
				with self.__db.transaction():
					msg = self.__msgs.get()
					if msg is Heartbeat:
						self.__heartbeat()
					else:
						self.__i_time = time.time()
						if msg['msg'] == "connect":
							self.__connect(msg)
						elif msg['msg'] == 'ability':
							self.__do_ability(msg)
						elif msg['msg'] == 'item':
							self.__do_item(msg)
						elif msg['msg'] == 'levelup':
							self.__level_up(msg)
						elif msg['msg'] == "disconnect":
							self.__disconnect(msg)					
						elif msg['msg'] == "join":
							self.__join(msg)
						elif msg['msg'] == "respec":
							self.__respec(msg)
						elif msg['msg'] == "action":
							self.__act(msg)
			except KeyboardInterrupt as ex:
				logging.log(f"Exiting server loop for {self.__clientid}...  (Interrupted)")
				for ws in self.__unames.values():
					try:
						ws.close()
					except:
						pass
							
		logging.log(f"Exiting main loop for {self.__clientid}")

	def heartbeat(self):
		try:
			while not self.__closed:
				self.__msgs.put(Heartbeat)
				asyncio.sleep(10)
		except KeyboardInterrupt:
			logging.log("Keyboard interrupt on heartbeat.")
		logging.log(f"Exiting heartbeat loop for {self.__clientid}")

	def __heartbeat(self):
		if len(self.__idmaps) == 0:			
			if time.time() - self.__i_time > DEACTIVE_TIME:
				logging.log(f"Shutting down a server for {self.__clientid}")
				self.__closed = True
		else:
			self.__i_time = time.time()
			now = time.time()
			if now - self.__last >= STEP_FREQUENCY:

				self.__last = now
				for m in self.__game.step():
					self.__handle_message(m)


				self.__handle_message(
						messages.TimeInfo(
							now=self.__last, 
							length=STEP_FREQUENCY,
							recv=tuple(self.__game.players)))


	def __disconnect(self, msg):
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


	def __handle_message(self, m):
		for (uname, s) in self.__unames.items():
			if uname in m.recv:
				for ws in s:
					ws.send(m.json)


	def __join(self, msg):		
		for m in self.__game.join(msg["socket"].uname):
			self.__handle_message(m)

	def __act(self, msg):
		for m in self.__game.action(msg['socket'].uname, msg['action']):
			self.__handle_message(m)

	def __respec(self, msg):
		cl = msg['data']
		p = self.__game.get_player(msg['socket'].uname)

		for m in self.__game.respec(p, cl):
			self.__handle_message(m)

	def connect(self, msg):
		for m in self.__game.connect(msg["uid"]):
			self.__handle_message(m)

		self.__handle_message(
			messages.TimeInfo(
				now=self.__last, 
				length=STEP_FREQUENCY,
				recv=(ws.uname,)))

	def __level_up(self, msg):
		p = self.__game.get_player(msg['socket'].uname)
		for m in p.level_up(msg['att']):
			self.__handle_message(m)


	def __do_ability(self, msg):
		for m in self.__game.use_ability(msg['socket'].uname, msg['ability'], msg['targets']):
			self.__handle_message(m)

	def __do_item(self, msg):
		for m in self.__game.use_item(msg['socket'].uname, msg['index'], msg['targets']):
			self.__handle_message(m)

GAME = Server()

eel.init("UI")

@eel.expose
def say_hello_py(x):
	print('Hello from %s' % x)

say_hello_py('Python World!')
#eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start("client/main.html")


