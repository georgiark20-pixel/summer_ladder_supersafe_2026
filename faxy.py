# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import webbrowser
from threading import Timer
from io import BytesIO
from Crypto.Cipher import AES
from mlkem.ml_kem import ML_KEM

app = Flask(__name__)
CORS(app)

ml_kem = ML_KEM()
users_db = {}
encrypted_vault = {}

# --- NEW: Serve your HTML file directly from the backend ---
@app.route('/')
def index():
    """Serves your frontend interface automatically at http://127.0.0.1:5000/"""
    return send_file('Faxy_project_v2.html')

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('id')
    username = data.get('name')
    if not user_id or not username:
        return jsonify({"error": "Missing ID or Username"}), 400
        
    ek, dk = ml_kem.key_gen()
    users_db[user_id] = {"name": username, "public_key": ek.hex(), "private_key": dk.hex()}
    
    print(f"\n[⚠️ QUANTUM KEY GEN] Generated CRYSTALS-Kyber key pair for: {username}")
    return jsonify({"status": "success"})

@app.route('/api/send', methods=['POST'])
def encrypt_and_send():
    if 'file' not in request.files:
        return jsonify({"error": "No file payload found"}), 400
        
    file = request.files['file']
    recipient_id = request.form.get('recipient_id')
    
    # Check if recipient exists, otherwise generate placeholder key for simulation
    if recipient_id in users_db:
        ek = bytes.fromhex(users_db[recipient_id]['public_key'])
    else:
        ek, _ = ml_kem.key_gen()
        
    file_bytes = file.read()
    
    # 1. Kyber Post-Quantum Encapsulation
    shared_secret, kyber_ciphertext = ml_kem.encaps(ek)
    
    # 2. AES-256-GCM Symmetric Encryption
    cipher = AES.new(shared_secret[:32], AES.MODE_GCM)
    ciphertext_bytes, tag = cipher.encrypt_and_digest(file_bytes)
    
    # --- THIS IS THE LOG YOU ARE LOOKING FOR ---
    print("\n" + "="*60)
    print("[🔒 POST-QUANTUM CRYPTO LOG]")
    print(f"📦 Encrypting File: {file.filename} ({len(file_bytes)} bytes)")
    print(f"🛡️ KEM Algorithm:  CRYSTALS-Kyber (ML-KEM-768)")
    print(f"🔑 Kyber Ciphertext Preview: {kyber_ciphertext.hex()[:40]}...")
    print(f"⚡ Symmetric Cipher: AES-256-GCM (Using Kyber Shared Secret)")
    print("="*60 + "\n")
    
    return jsonify({"status": "success"})

def launch_browser():
    """Helper to open the browser automatically after the server boots up."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    print("\n--- Booting Faxy PQC Engine ---")
    # Wait 1.5 seconds for Flask to spin up, then open the browser automatically
    Timer(1.5, launch_browser).start()
    app.run(debug=True, port=5000, use_reloader=False)