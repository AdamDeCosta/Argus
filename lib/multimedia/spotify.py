import aiohttp
import json
import base64


async def get_auth(client):
    b64_key = base64.b64encode(client.sp_key.encode('ascii')).decode('ascii')
    params = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(b64_key)
    }
    r = await client.session.request('POST',
                                     'https://accounts.spotify.com/api/token',
                                     params=params,
                                     headers=headers)
    resp = await r.text()
    resp = json.loads(resp)
    token = resp['access_token']
    return token
