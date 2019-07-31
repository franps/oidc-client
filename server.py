import json
import requests
from authlib.flask.client import OAuth
from flask import Flask, redirect, request, render_template, session, jsonify
from functools import wraps

redirect_uri = 'http://localhost:3000/callback'

app = Flask(__name__)
app.secret_key = 'SecretKey'
app.debug = True

oauth = OAuth(app)
client = oauth.register(
    'client',
    client_id='xxx',
    client_secret='xxx',
    api_base_url='https://auth-testing.iduruguay.gub.uy/oidc/v1',
    access_token_url='https://auth-testing.iduruguay.gub.uy/oidc/v1/token',
    authorize_url='https://auth-testing.iduruguay.gub.uy/oidc/v1/authorize',
    client_kwargs={
        'scope': 'openid email',
    },
)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    code = request.args.get('code')
    state = request.args.get('state')
    print(session)
    return render_template('success.html', code=code, state=state)

# https://oauthlib.readthedocs.io/en/latest/oauth2/clients/webapplicationclient.html
# https://flask-oauthlib.readthedocs.io/en/latest/client.html
@app.route('/accessToken/<code>')
def request_accessToken(code):
    # print('https://auth-testing.iduruguay.gub.uy/oidc/v1/token')
    headers = {'Authorization': 'Basic xxxx',
               'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'code': str(code), 'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri}
    req = requests.post(
        'https://auth-testing.iduruguay.gub.uy/oidc/v1/token', headers=headers, data=body)
    print(req)
    #token = client.authorize_access_token(code=code)
    # print(token)
    return "success"


@app.route('/login')
def login():
    return client.authorize_redirect(redirect_uri=redirect_uri)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
