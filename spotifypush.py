import requests #to get data from ishpotify
import os #to interact with the github secrets


#github secrets are pretty cool. They can simulate an environment. nice. 
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['SPOTIFY_REFRESH_TOKEN']


#spotify doesn't give a master token for profile access, even though there's one for general access
#instead, there's a expiring refresh token that needs to be sent 

#getting the access_token from the client endpoint, which returns the access token
authtok = requests.post("https://accounts.spotify.com/api/token" , {
    'grant_type' : 'refresh_token',
    'refresh_token':REFRESH_TOKEN,
    'client_id':CLIENT_ID,
    'client_secret':CLIENT_SECRET
    })

access_token = authtok.json()['access_token']

#make header via access token 
prover = {'Authorization' : f'Bearer {access_token}'}

#send the request , returns top 5 artists  
req = requests.get("https://api.spotify.com/v1/me/top/artists?limit=5", headers=prover)

#turn respose to markdown and put it in the readme
artists = req.json()['items']
artistsmd = [];

for x in artists :
    name = x['name']
    #url = x['external_urls']['spotify']
    #icon = x['images'][0] if x['images'] else 'https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books/blob/master/Quantum%20Computing/Frieren_Practical_Quantum_Computing_For_Developers.png?raw=true'
    templine = f'"{name}",'
    artistsmd.append(templine);

with open('README.md', 'r+') as file:
    lines = file.readlines()
    start = lines.index("Listening_to(Mostly):[\n")
    end = lines.index("]\n")
    lines[start+1:end] = [x for x in artistsmd]
    file.seek(0)
    file.writelines(lines)
    file.truncate()
