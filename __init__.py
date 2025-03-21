from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Votre page d'accueil

# Route d'encryptage (la clé est générée automatiquement)
@app.route('/encrypt/', methods=['POST'])
def encrypt_value():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"error": "Veuillez fournir la valeur à chiffrer."}), 400
    try:
        # Génération d'une nouvelle clé Fernet
        key = Fernet.generate_key()
        fernet = Fernet(key)
        token = fernet.encrypt(data['value'].encode())
        # On renvoie à l'utilisateur le token et la clé (la clé devra être sauvegardée pour la décryption)
        return render_template('encrypt.html', token=token.decode(), key=key.decode())
    except Exception as e:
        return jsonify({"error": "Erreur lors de l'encryptage.", "details": str(e)}), 400

# Route de décryptage (l'utilisateur doit fournir la clé générée précédemment et le token)
@app.route('/decrypt/', methods=['POST'])
def decrypt_value():
    data = request.get_json()
    if not data or 'value' not in data or 'key' not in data:
        return jsonify({"error": "Veuillez fournir la clé et la valeur à déchiffrer."}), 400
    try:
        user_key = data['key']
        fernet = Fernet(user_key.encode())
        decrypted_bytes = fernet.decrypt(data['value'].encode())
        decrypted_value = decrypted_bytes.decode()
        return render_template('decrypt.html', result=decrypted_value)
    except Exception as e:
        return jsonify({"error": "Erreur lors de la décryption.", "details": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True) #action
