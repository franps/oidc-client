import base64
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
        'scope': 'openid email personal_info auth_info',
    },
)


def sendtokenreq(code):
    headers = {'Authorization': 'Basic xxx',
               'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'code': str(code), 'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri}
    toreturn = [False, {}]
    try:
        req = requests.post(
            'https://auth-testing.iduruguay.gub.uy/oidc/v1/token', headers=headers, data=body, verify=False)
        toreturn[0] = True
        toreturn[1] = req.json()
    except requests.exceptions.ConnectionError:
        toreturn[0] = False
        toreturn[1] = "Connection refused"
    return toreturn


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    code = request.args.get('code')
    state = request.args.get('state')
    print(session)
    return render_template('code.html', code=code, state=state)


@app.route('/accessToken/<code>')
def request_accessToken(code):
    response = sendtokenreq(code)
    if response:
        body = response[1]
        idtok = body.get('id_token')

        return render_template('userinfo.html', token=idtok)


@app.route('/decodejwt/<token>')
def decodejwt(token):
    idtk = token.split(".")[1]
    i = len(idtk) % 4
    while(i > 0):
        idtk += "="
        i -= 1
    print(idtk)
    data = base64.b64decode(idtk)
    return render_template('userinfo.html', token=data)


@app.route('/login')
def login():
    return client.authorize_redirect(redirect_uri=redirect_uri)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
