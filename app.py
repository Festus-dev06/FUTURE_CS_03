import os
import io
import base64
from flask import Flask, request, render_template, redirect, url_for, flash, send_file, abort
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv

# Load env (.env) if present
load_dotenv()

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Limit upload size (10 MB)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Flask secret
FLASK_SECRET = os.environ.get("FLASK_SECRET") or os.urandom(16).hex()
app.secret_key = FLASK_SECRET

# AES key (base64 in .env)
AES_KEY_B64 = os.environ.get("AES_KEY_BASE64")
AES_KEY = base64.b64decode(AES_KEY_B64) if AES_KEY_B64 else get_random_bytes(32)

# --- AES helpers ---
def encrypt_bytes(plaintext: bytes) -> bytes:
    nonce = get_random_bytes(12)
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + tag + ciphertext

def decrypt_bytes(blob: bytes) -> bytes:
    nonce, tag, ciphertext = blob[:12], blob[12:28], blob[28:]
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("index"))
        filename = secure_filename(file.filename)
        enc_blob = encrypt_bytes(file.read())
        with open(os.path.join(UPLOAD_FOLDER, filename + ".enc"), "wb") as f:
            f.write(enc_blob)
        flash(f"Uploaded & encrypted {filename}", "success")
        return redirect(url_for("index"))

    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".enc")]
    return render_template("index.html", files=files)

@app.route("/download/<path:enc_filename>")
def download(enc_filename):
    safe = secure_filename(enc_filename)
    path = os.path.join(UPLOAD_FOLDER, safe)
    if not os.path.isfile(path):
        abort(404)
    with open(path, "rb") as f:
        blob = f.read()
    dec = decrypt_bytes(blob)
    original = safe[:-4] if safe.endswith(".enc") else safe
    return send_file(io.BytesIO(dec), as_attachment=True, download_name=original)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
