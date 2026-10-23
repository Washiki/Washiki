import os
import secrets
import threading
import webbrowser
import requests

from flask import Flask, request

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""
SCOPE = "user-top-read"

state = secrets.token_urlsafe(16)
app = Flask(__name__)
auth_code = {}

@app.route("/callback")
def callback():
    if request.args.get("state") != state:
        return "State mismatch. Authorization rejected.", 400

    if "error" in request.args:
        return f"Authorization failed: {request.args['error']}", 400

    auth_code["code"] = request.args.get("code")
    return "Spotify authorization successful. You can close this tab."

def run_server():
    app.run(host="127.0.0.1", port=8888, debug=False, use_reloader=False)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()

# Wait for the local server to start.
import time
time.sleep(1)

url = "https://accounts.spotify.com/authorize"
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "state": state
}

webbrowser.open(requests.Request("GET", url, params=params).prepare().url)

print("Authorize Spotify in your browser.")
print("Waiting for authorization...")

while "code" not in auth_code:
    time.sleep(0.5)

response = requests.post(
    "https://accounts.spotify.com/api/token",
    data={
        "grant_type": "authorization_code",
        "code": auth_code["code"],
        "redirect_uri": REDIRECT_URI
    },
    auth=(CLIENT_ID, CLIENT_SECRET),
    timeout=15
)

response.raise_for_status()
tokens = response.json()

print("\nYour new refresh token:")
print(tokens["refresh_token"])
