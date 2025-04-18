from flask import Flask, jsonify, request
import jwt, time, requests, gzip
from io import BytesIO

KEY_ID = '8QGP6V5V8G'
ISSUER_ID = '69a6de6f-dd67-47e3-e053-5b8c7c11a4d1'
PRIVATE_KEY_PATH = 'AuthKey_8QGP6V5V8G.p8'
VENDOR_NUMBER = '85040982'

app = Flask(__name__)

@app.route('/report')
def get_report():
    try:
        with open(PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()

        headers = {
            "alg": "ES256",
            "kid": KEY_ID,
            "typ": "JWT"
        }

        payload = {
            "iss": ISSUER_ID,
            "exp": int(time.time()) + 1200,
            "aud": "appstoreconnect-v1"
        }

        token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)

        # Always use yesterday's date dynamically
        report_date = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 86400))

        url = (
            "https://api.appstoreconnect.apple.com/v1/salesReports?"
            "filter[reportType]=SALES&"
            "filter[reportSubType]=SUMMARY&"
            "filter[frequency]=DAILY&"
            f"filter[reportDate]={report_date}&"
            f"filter[vendorNumber]={VENDOR_NUMBER}"
        )

        resp = requests.get(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/a-gzip"
        })

        if resp.status_code != 200:
            return jsonify({"error": resp.text}), 500

        buffer = BytesIO(resp.content)
        with gzip.GzipFile(fileobj=buffer) as gz:
            unzipped = gz.read().decode("utf-8")

        return unzipped

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()