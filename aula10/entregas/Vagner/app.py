# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import bcrypt
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões e mensagens flash

def carregar_usuarios():
    with open('usuarios.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha').encode('utf-8')

        usuarios = carregar_usuarios()

        hashsenha = hashlib.sha256(senha.encode()).hexdigest()

        if hashsenha == usuarios[usuario]:
            session['usuario_logado'] = usuario
            return redirect(url_for('sucesso'))
        else:
            flash('Credenciais inválidas. Tente novamente!', 'error')
    
    return render_template('login.html')

@app.route('/sucesso')
def sucesso():
    if 'usuario_logado' in session:
        return render_template('sucesso.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)