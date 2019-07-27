import json
from authlib.flask.client import OAuth
from flask import Flask, redirect, request, render_template, session
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
    access_token_url='https://auth-testing.iduruguay.gub.uy/oidc/v1/oauth/token',
    authorize_url='https://auth-testing.iduruguay.gub.uy/oidc/v1/authorize',
    client_kwargs={
        'scope': 'openid',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'openid' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    # client.authorize_access_token() #parse_request_uri_response(uri, state)
    code = request.args.get('code')
    state = request.args.get('state')
    print(session)
    return render_template('success.html', code=code, state=state)

# https://oauthlib.readthedocs.io/en/latest/oauth2/clients/webapplicationclient.html
# https://flask-oauthlib.readthedocs.io/en/latest/client.html
@app.route('/accessToken')
def request_accessToken():
    #prepare_request_body(code=None, redirect_uri=None, body='', include_client_id=True, **kwargs)
    return "success"


@app.route('/login')
def login():
    return client.authorize_redirect(redirect_uri=redirect_uri)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
