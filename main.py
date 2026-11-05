from http.server import BaseHTTPRequestHandler, HTTPServer
import json, urllib.parse, threading, time

status = {"etat": "Deconnecte", "log": ["En attente"], "config": ""}

HTML = """<html><head><meta name="viewport" content="width=device-width"><title>SHADOW TUNNEL</title>
<style>body{background:#0f0f0f;color:white;text-align:center;font-family:sans-serif;padding:15px}
textarea{width:95%;height:100px;border-radius:10px;padding:10px;background:#222;color:#0f0;border:none}
button{padding:15px;width:95%;border:none;border-radius:10px;font-size:18px;margin-top:10px;color:white}
#b1{background:green}#b2{background:#c00;margin-top:5px}
#log{background:#000;color:#0f0;text-align:left;padding:10px;border-radius:10px;height:180px;overflow:auto;font-size:13px;margin-top:10px}
</style></head><body>
<h1>SHADOW TUNNEL</h1>
<p id="s" style="font-size:20px">Deconnecte</p>
<textarea id="c" placeholder="Colle ta config vless ou vmess ici"></textarea><br>
<button id="b1" onclick="connect()">CONNECTER</button>
<button id="b2" onclick="deconnect()">DECONNECTER</button>
<div id="log"></div>
<script>
async function refresh(){let r=await fetch("/status");let j=await r.json();document.getElementById("s").innerText=j.etat;document.getElementById("log").innerHTML=j.log.join("<br>")}
async function connect(){let c=document.getElementById("c").value;await fetch("/connect",{method:"POST",body:"config="+encodeURIComponent(c)});refresh()}
async function deconnect(){await fetch("/disconnect",{method:"POST"});refresh()}
setInterval(refresh,1500);refresh();
</script></body></html>"""

def addLog(m):
    status["log"].append(time.strftime("%H:%M:%S") + " - " + m)
    status["log"] = status["log"][-20:]

def fakeConnect(cfg):
    status["etat"] = "Connexion..."
    addLog("Lecture config...")
    time.sleep(1)
    if not cfg or "://" not in cfg:
        status["etat"] = "Erreur"
        addLog("Config invalide. Colle vless ou vmess")
        return
    open("config.txt", "w").write(cfg)
    status["config"] = cfg[:30]
    addLog("Config sauvegardee dans config.txt")
    addLog("Resolution serveur...")
    time.sleep(1)
    addLog("Handshake TLS...")
    time.sleep(1)
    addLog("Tunnel etabli")
    status["etat"] = "Connecte"

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())
    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(ln).decode()
        d = urllib.parse.parse_qs(body)
        if self.path == "/connect":
            cfg = d.get("config", [""])[0]
            threading.Thread(target=fakeConnect, args=(cfg,), daemon=True).start()
        if self.path == "/disconnect":
            status["etat"] = "Deconnecte"
            addLog("Deconnecte par utilisateur")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *a):
        pass

print("Ouvre Chrome vers http://localhost:8550")
HTTPServer(("0.0.0.0", 8550), H).serve_forever()
