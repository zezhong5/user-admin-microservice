import os
#from flask_oauthlib.client import OAuth
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

# github = oauth.register(
#     'github',
#     client_id='c0360adb3cbda91a58fa',
#     client_secret='27ea383b58b652d5acf67d74aa87e7797e527e9c',
#     access_token_url="https://github.com/login/oauth/access_token",
#     access_token_params=None,
#     authorize_url="https://github.com/login/oauth/authorize",
#     authorize_params=None,
#     api_base_url="https://api.github.com/",
#     client_kwargs={"scope": "user:email"},
# )

github = oauth.register(
    'github',
    client_id='',
    client_secret='',
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

google = oauth.register(
    name="google",
    client_id=os.environ.get('GOOGLE_OAUTH_API_KEY'),
    client_secret=os.environ.get('GOOGLE_OAUTH_API_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid profile email"},
)