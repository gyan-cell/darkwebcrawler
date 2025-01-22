from flask import Flask, redirect, request, session, jsonify
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
app.config["SESSION_TYPE"] = "filesystem"

# App ID Configuration

REDIRECT_URI = "https://au-syd.appid.cloud.ibm.com/oauth/v4/37e46843-2380-412b-864d-d0ca533d3e8c/IBMid/callback"


clientId = "cc1146fc-d1d5-43bc-9aa0-898c84707582"
tenantId = "37e46843-2380-412b-864d-d0ca533d3e8c"
secret = "NjUxMGJlNDQtYWQzNy00N2ZlLWI1NzItZDEyMjg0NmVkN2Y4"
oAuthServerUrl = (
    "https://au-syd.appid.cloud.ibm.com/oauth/v4/37e46843-2380-412b-864d-d0ca533d3e8c"
)
profilesUrl = "https://au-syd.appid.cloud.ibm.com"
discoveryEndpoint = "https://au-syd.appid.cloud.ibm.com/oauth/v4/37e46843-2380-412b-864d-d0ca533d3e8c/.well-known/openid-configuration"


# Routes
@app.route("/")
def index():
    if "user" in session:
        return f"Welcome, {session['user']['name']}! <a href='/logout'>Logout</a>"
    return '<a href="/login">Login with App ID</a>'


@app.route("/login")
def login():
    auth_url = f"{oAuthServerUrl}/authorization?client_id={clientId}&response_type=code&redirect_uri={REDIRECT_URI}&scope=openid"
    return redirect(auth_url)


@app.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed.", 400

    # Exchange the authorization code for tokens
    token_url = f"{oAuthServerUrl}/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": clientId,
        "client_secret": secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = requests.post(token_url, data=payload, headers=headers)
    if token_response.status_code != 200:
        return f"Token exchange failed: {token_response.text}", 400

    tokens = token_response.json()
    id_token = tokens["id_token"]
    user_info = requests.get(
        f"{oAuthServerUrl}/userinfo",
        headers={"Authorization": f"Bearer {id_token}"},
    ).json()

    print(user_info)

    # Save user info in the session
    session["user"] = user_info
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5511)
