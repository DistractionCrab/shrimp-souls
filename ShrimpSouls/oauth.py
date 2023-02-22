import requests
import aiohttp
import os
import json
import jwt
import base64
import asyncio
import ShrimpSouls.logging as logging

CLIENT_ID = "ec767p01w3r37lrj9gfvcz9248ju9v"

class Secrets:
	def __init__(self):
		self.__f = open(os.path.join(os.environ["SS_SSL_PATH"], "APP_SECRET.json"), 'r')
		self.__secrets = json.loads(self.__f.read())

	def __getitem__(self, i):
		return self.__secrets[i]

	def update_oauth(self, oauth):
		self.__secrets["oauth_token"] = oauth
		self.__f.write(json.dumps(self.__secrets))
		self.__f.flush()
		logging.log("Updated OAuth Token.")

SECRETS = Secrets()

HEADERS = {
	'Content-Type': "application/x-www-form-urlencoded"
}
TOKEN_URL ='https://id.twitch.tv/oauth2/token'
TOKEN_DATA = "client_id={c_id}&client_secret={app_secret}&grant_type=client_credentials"

def jwt_secret():
	return base64.b64decode(SECRETS["jwt_secret"])

def parse_jwt(msg):
	s = jwt_secret()
	try:
		return jwt.decode(msg['token'], jwt_secret(), algorithms=["HS256"])
	except:
		return None

class TwitchOAuth:
	def __init__(self):
		self.__app_secret = SECRETS["server_secret"]
		self.__jwt_secret = SECRETS["jwt_secret"]
		self.__oauth_token = SECRETS["oauth_token"]
		self.__oauth_lock = asyncio.Event()

	async def __fetch_token(self):
			# If the event isn't set, that means that some other task is attempting to fix OAuth.
			if not self.__oauth_lock.is_set():
				logging.log("Waiting on OAuth Update...")
				self.__oauth_lock.wait()
			else:
				# Attempt the get a new OAuth Token, may need multiple attempts if there are server issues.
				logging.log("Attempting to renew OAuth Token.")
				self.__oauth_lock.clear()
				try:
					async with aiohttp.ClientSession() as session:
						resolved = False
						while not resolved:
							r = await session.post(
								TOKEN_URL,
								headers=HEADERS,
								data=DATA.format(CLIENT_ID, self.__app_secret))
							if v.status_code == 200:
								v = json.loads(await r.text())
								global SECRETS
								SECRETS.update_oauth(v["access_token"])
								self.__oauth_lock.set()
								return v
							elif v.status_code == 400:
								logging.log(f"TwitchAPI request failed (Renewing Token): {v} ({v.status_code})")
								self.__oauth_lock.set()
							else:
								logging.log(f"Error code for TwitchAPI request: {v} ({v.status_code})")
								self.__oauth_lock.set()
								return None

							# Wait for 10 minutes before trying again, likely remote
							# issues from Twitch.
							asyncio.sleep(600)
				except:
					self.__oauth_lock.set()
					return None

	async def get_username(self, i):
		try:
			async with aiohttp.ClientSession() as session:
				url = f'https://api.twitch.tv/helix/users?id={i}'
				headers = {
					"Authorization": "Bearer " + self.__oauth_token,
					"Client-ID": CLIENT_ID,
				}
				r = await session.get(url, headers=headers)
				if r.status == 200:
					return json.loads(await r.text())
				elif r.status == 401:
					await self.__fetch_token()
					return await self.get_username(i)
				else:
					logging.log(f"Failed to get username: {i} ({r.text})")
					return None
		except Exception as ex:
			logging.log(f"Exception in fetching username: {ex}")
			return None

OAUTH = TwitchOAuth()


def update_ip():
	""" Used to update the domain mapping for our servers IP address. """
	username = input("Username: ")
	password = input("Password: ")
	ip = "82.180.173.104"
	subdomain = "shrimpsouls.distractioncrab.net"
	URL = f"https://{username}:{password}@domains.google.com/nic/update?hostname={subdomain}&myip={ip}"

	r = requests.post(URL)