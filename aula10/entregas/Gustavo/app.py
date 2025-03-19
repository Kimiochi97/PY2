# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
with open('usuarios.json', 'r') as f:
    print(json.load(f))

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões e mensagens flash

# Usuário mockado para exemplo (em produção use banco de dados)
USUARIO_VALIDO = {
    'usuario': 'admin',
    'senha': 'secret'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == USUARIO_VALIDO['usuario'] and senha == USUARIO_VALIDO['senha']:
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