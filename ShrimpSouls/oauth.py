import requests
import aiohttp
import os
import json
import jwt
import base64
import asyncio
import traceback
import ShrimpSouls.logging as logging

CLIENT_ID = "CLIENT_SECRET_FROM_TWITCH"

class Secrets:
	def __init__(self):
		f = open(os.path.join(os.environ["SS_SSL_PATH"], "APP_SECRET.json"), 'r')
		self.__secrets = json.loads(f.read())

	def __getitem__(self, i):
		return self.__secrets[i]

	def update_oauth(self, oauth):
		f = open(os.path.join(os.environ["SS_SSL_PATH"], "APP_SECRET.json"), 'w')
		self.__secrets["oauth_token"] = oauth
		f.write(json.dumps(self.__secrets, indent=4))
		f.flush()
		f.close()
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
		self.__oauth_lock = asyncio.Lock()

	async def __fetch_token(self):
			# If the event isn't set, that means that some other task is attempting to fix OAuth.
			if self.__oauth_lock.locked():
				t = asyncio.current_task()
				logging.log(f"Waiting on OAuth Update... {str(t.get_name())}")
				await self.__oauth_lock.acquire()
				self.__oauth_lock.release()
			else:
				async with self.__oauth_lock:
					# Attempt the get a new OAuth Token, may need multiple attempts if there are server issues.
					logging.log("Attempting to renew OAuth Token.")
					try:
						async with aiohttp.ClientSession() as session:
							resolved = False
							while not resolved:
								r = await session.post(
									TOKEN_URL,
									headers=HEADERS,
									data=TOKEN_DATA.format(c_id=CLIENT_ID, app_secret=SECRETS["server_secret"]))
								if r.status == 200:
									v = json.loads(await r.text())
									SECRETS.update_oauth(v["access_token"])
									return v
								elif r.status == 400:
									logging.log(f"TwitchAPI request failed (Renewing Token): {v} ({v.status_code})")
								else:
									logging.log(f"Error code for TwitchAPI request: {v} ({v.status_code})")
									return None

								# Wait for 10 minutes before trying again, likely remote
								# issues from Twitch.
								asyncio.sleep(600)
					except Exception as ex:						
						return None

	async def get_username(self, i):
		try:
			async with aiohttp.ClientSession() as session:
				url = f'https://api.twitch.tv/helix/users?id={i}'
				headers = {
					"Authorization": "Bearer " + SECRETS["oauth_token"],
					"Client-ID": CLIENT_ID,
				}
				r = await session.get(url, headers=headers)
				if r.status == 200:
					return json.loads(await r.text())
				elif r.status == 401:
					await self.__fetch_token()
					#return await self.get_username(i)
					return None
				else:
					logging.log(f"Failed to get username: {i} ({r.text})")
					return None
		except Exception as ex:
			logging.log(f"Exception in fetching username: {ex}")
			print(traceback.format_exc())
			return None

OAUTH = TwitchOAuth()


def update_ip():
	"""
	Used to update the domain mapping for our servers IP address.
	This uses Google's Domain services.
	"""
	username = input("Username: ")
	password = input("Password: ")
	ip = "IP ADDRESS HERE"
	subdomain = "DOMAIN ADDRESS HERE"
	URL = f"https://{username}:{password}@domains.google.com/nic/update?hostname={subdomain}&myip={ip}"

	r = requests.post(URL)