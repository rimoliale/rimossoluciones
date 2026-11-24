from http.server import BaseHTTPRequestHandler
import json
import os
import mercadopago

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

        # Toma el token desde las Environment Variables de Vercel (MP_ACCESS_TOKEN)
        access_token = os.environ.get("MP_ACCESS_TOKEN", "APP_USR-5475076937715503-112413-82d85dd16a4179c521d325d78d8b7402-178952498")
        sdk = mercadopago.SDK(access_token)

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

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"init_point": preference["init_point"]}).encode('utf-8'))