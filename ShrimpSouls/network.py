import requests

CLIENT_ID = "ec767p01w3r37lrj9gfvcz9248ju9v"

HEADERS = {
	'Content-Type': "application/x-www-form-urlencoded"
}

DATA = {
	"client_id": CLIENT_ID,
	"client_secret": APP_SECRET,
	"grant_type": "client_credentials"
}

DATA = f"client_id={CLIENT_ID}&client_secret={APP_SECRET}&grant_type=client_credentials"

REQUEST_URL ='https://id.twitch.tv/oauth2/token'

def get_token():
	r = requests.post(REQUEST_URL, headers=HEADERS, data=DATA)
	print(r.text)



EXAMPLE_ID = 150659682
EXAMPLE_ID = 265737932

def get_username():
	r = requests.get(
		f'https://api.twitch.tv/helix/users?id={EXAMPLE_ID}',
		headers={
			"Authorization": "Bearer " + ACCESS_TOKEN['access_token'],
			"Client-ID": CLIENT_ID,
		}
	)
	print(r)
	print(r.text)

#print(get_token())
get_username()