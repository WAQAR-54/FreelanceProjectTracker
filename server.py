# server.py
import os, smtplib, ssl, json
from email.message import EmailMessage
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# ---- Edit these or set as environment variables ----
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.zoho.com")     # or "smtppro.zoho.com"
SMTP_PORT   = int(os.getenv("SMTP_PORT", "465"))            # 465=SSL, 587=STARTTLS
SMTP_USER   = os.getenv("SMTP_USERNAME", "you@yourdomain.com")
SMTP_PASS   = os.getenv("SMTP_PASSWORD", "your_app_password")
SENDER      = os.getenv("SENDER_EMAIL", SMTP_USER)

def send_via_smtp(receiver: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    ctx = ssl.create_default_context()
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)

class Handler(SimpleHTTPRequestHandler):
    # Serve index.html by default
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/index.html"
        return super().doGET()

    # Handle form POST to /send
    def do_POST(self):
        if self.path != "/send":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        data   = self.rfile.read(length).decode("utf-8")

        # Supports form-urlencoded and JSON
        if "application/json" in self.headers.get("Content-Type", ""):
            payload = json.loads(data or "{}")
        else:
            payload = {k: v[0] for k, v in parse_qs(data).items()}

        to      = (payload.get("to") or "").strip()
        subject = (payload.get("subject") or "Hello").strip()
        body    = (payload.get("body") or "").strip()

        if not to or not body:
            self._json({"ok": False, "error": "Missing 'to' or 'body'."}, 400)
            return

        try:
            send_via_smtp(to, subject, body)
            self._json({"ok": True, "message": f"Email sent to {to}"})
        except smtplib.SMTPAuthenticationError as e:
            self._json({"ok": False, "error": f"SMTP auth failed: {e}"}, 401)
        except Exception as e:
            self._json({"ok": False, "error": str(e)}, 500)

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        # Allow fetch from same origin file
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    # Small fix: Python's SimpleHTTPRequestHandler uses do_GET name
    def doGET(self):  # wrapper for our custom default path logic
        return super().do_GET()

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8000
    print(f"Running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
