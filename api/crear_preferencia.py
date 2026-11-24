from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        access_token = os.environ.get("MP_ACCESS_TOKEN", "").strip()

        preference_data = {
            "items": [
                {
                    "title": data["title"],
                    "description": data.get("description", ""),
                    "picture_url": data.get("picture_url", ""),
                    "quantity": 1,
                    "unit_price": float(data["price"]),
                    "currency_id": "ARS"
                }
            ],
            "back_urls": {
                "success": "https://www.rimossoluciones.com.ar/ElGaragedeRimo",
                "failure": "https://www.rimossoluciones.com.ar/ElGaragedeRimo",
                "pending": "https://www.rimossoluciones.com.ar/ElGaragedeRimo"
            },
            "auto_return": "approved"
        }

        req = urllib.request.Request(
            "https://api.mercadopago.com/checkout/preferences",
            data=json.dumps(preference_data).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                mp_response = json.loads(resp.read().decode("utf-8"))
                status_code = 200
                body = {"init_point": mp_response.get("init_point")}
        except urllib.error.HTTPError as e:
            status_code = e.code
            body = {"error": e.read().decode("utf-8")}

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode('utf-8'))