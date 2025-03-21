from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Votre page d'accueil

# Génération de la clé de chiffrement (à stocker de façon sécurisée en production)
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Chiffre la valeur
    # On passe le token au template encrypt.html
    return render_template('encrypt.html', token=token.decode())

@app.route('/decrypt/', methods=['POST'])
def decrypt_value():
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"error": "Clé 'value' manquante dans la requête."}), 400
    try:
        decrypted_bytes = f.decrypt(data['value'].encode())
        decrypted_value = decrypted_bytes.decode()
        # On passe le résultat au template decrypt.html
        return render_template('decrypt.html', result=decrypted_value)
    except Exception:
        return jsonify({"error": "La décryption a échoué. Vérifiez que la valeur est correcte."}), 400

if __name__ == "__main__":
    app.run(debug=True)
