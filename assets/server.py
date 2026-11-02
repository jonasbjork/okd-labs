"""Liten övningsserver. Endast avsedd för laborationsmiljön."""
import hashlib
import hmac
import json
import os
from pathlib import Path
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import URLError
from urllib.request import urlopen


CONFIG_DIR = Path(os.getenv("CONFIG_DIR", "/etc/lab-config"))
SECRET_DIR = Path(os.getenv("SECRET_DIR", "/etc/lab-secret"))
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
FLAG_DIR = Path(os.getenv("FLAG_DIR", "/tmp"))


def read(path, default=""):
    try:
        return Path(path).read_text().strip()
    except FileNotFoundError:
        return default


def token():
    return os.getenv("LAB_TOKEN") or read(SECRET_DIR / "token")


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, value):
        body = (json.dumps(value, ensure_ascii=False) + "\n").encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/ready", "/live"):
            flag = FLAG_DIR / ("not-ready" if path == "/ready" else "fail-live")
            ok = not Path(flag).exists()
            self.reply(200 if ok else 503, {"ok": ok})
        elif path == "/work":
            hashlib.pbkdf2_hmac("sha256", b"lab", b"salt", 200000)
            self.reply(200, {"work": "done", "hostname": socket.gethostname()})
        elif path == "/state":
            self.reply(200, {"value": read(DATA_DIR / "state.txt")})
        elif path == "/backend":
            url = os.getenv("BACKEND_URL", "")
            if not url:
                self.reply(503, {"error": "BACKEND_URL saknas"})
                return
            try:
                with urlopen(url, timeout=3) as response:
                    result = json.load(response)
                self.reply(200, {"backend": result})
            except (URLError, ValueError, TimeoutError):
                self.reply(502, {"error": "Backend kunde inte nås"})
        elif path == "/":
            self.reply(200, {
                "message": os.getenv("MESSAGE", "Hej från OKD"),
                "file_message": read(CONFIG_DIR / "message"),
                "version": os.getenv("APP_VERSION", "v1"),
                "secret_loaded": bool(token()),
                "hostname": socket.gethostname(),
            })
        else:
            self.reply(404, {"error": "Okänd sökväg"})

    def do_POST(self):
        if self.path != "/state":
            self.reply(404, {"error": "Okänd sökväg"})
            return
        expected = token()
        if not expected or not hmac.compare_digest(self.headers.get("X-Lab-Token", ""), expected):
            self.reply(403, {"error": "Fel token"})
            return
        size = int(self.headers.get("Content-Length", "0"))
        if not 0 < size <= 4096:
            self.reply(400, {"error": "Skicka 1–4096 byte"})
            return
        try:
            (DATA_DIR / "state.txt").write_text(self.rfile.read(size).decode())
        except (OSError, UnicodeError):
            self.reply(500, {"error": "Kunde inte skriva till /data"})
            return
        self.reply(200, {"saved": True})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
