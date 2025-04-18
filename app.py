from flask import Flask, jsonify
import jwt, time

KEY_ID = '8QGP6V5V8G'
ISSUER_ID = '69a6de6f-dd67-47e3-e053-5b8c7c11a4d1'
PRIVATE_KEY_PATH = 'AuthKey_8QGP6V5V8G.p8'

app = Flask(__name__)

@app.route('/token')
def get_token():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()

    headers = { "alg": "ES256", "kid": KEY_ID, "typ": "JWT" }
    payload = {
        "iss": ISSUER_ID,
        "exp": int(time.time()) + 1200,
        "aud": "appstoreconnect-v1"
    }

    token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
    return jsonify(token=token)

if __name__ == '__main__':
    app.run()