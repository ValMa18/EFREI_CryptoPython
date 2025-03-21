from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3


app = Flask(name)

@app.route('/')
def home():
    return "<h1>Bienvenue sur l'API CryptoPython</h1>"

@app.route('/encrypt/<string:key>/<string:message>')
def encrypt_message(key, message):
    try:
        key_bytes = key.encode()  # Convertir la clé en bytes
        f = Fernet(key_bytes)  # Créer un objet Fernet avec cette clé
        encrypted = f.encrypt(message.encode())  # Chiffrer le message
        return encrypted.decode()  # Retourne le message chiffré
    except Exception as e:
        return f"Erreur : {str(e)}"

@app.route('/decrypt/<string:key>/<string:token>')
def decrypt_message(key, token):
    try:
        key_bytes = key.encode()  # Convertir la clé en bytes
        f = Fernet(key_bytes)  # Créer un objet Fernet avec cette clé
        decrypted = f.decrypt(token.encode())  # Déchiffrer le message
        return decrypted.decode()  # Retourne le message déchiffré
    except Exception as e:
        return f"Erreur : {str(e)}"

if name == "main":
    app.run(debug=True)
