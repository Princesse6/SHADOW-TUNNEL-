from http.server import BaseHTTPRequestHandler, HTTPServer

HTML = """
<html><head><meta name='viewport' content='width=device-width'><title>Mon Tunnel</title>
<style>body{background:#111;color:white;text-align:center;font-family:sans-serif;padding:20px}
textarea{width:90%;height:120px;border-radius:10px;padding:10px}
button{background:green;color:white;padding:15px;width:90%;border:none;border-radius:10px;font-size:18px;margin-top:10px}
</style></head><body>
<h1>MON TUNNEL</h1>
<textarea id='c' placeholder='Colle ta config ici vless:// vmess:// wireguard...'></textarea><br>
<button onclick="document.getElementById('s').innerText='Connexion en cours...';document.getElementById('s').style.color='lime'">CONNECTER</button>
<p id='s' style='color:red'>Déconnecté</p>
</body></html>
"""

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-type","text/html"); self.end_headers()
        self.wfile.write(HTML.encode())
    def log_message(self, *a): pass

print("Ouvre Chrome -> http://localhost:8550")
HTTPServer(("0.0.0.0", 8550), H).serve_forever()
