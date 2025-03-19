from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tarefa(db.Model):
    """Modelo para representar uma tarefa"""
    id = db.Column(db.Integer, primary_key=True)
    tarefa = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.Integer)

    def __repr__(self):
        return f'<Tarefa {self.tarefa}>'

@app.route('/')
def index():
    tarefas = Tarefa.query.all()
    return render_template('tarefas.html', tarefas=tarefas)

@app.route('/add', methods=['POST'])
def add_tarefa():
    tarefa = request.form.get('tarefa')
    descricao = request.form.get('descricao')
    duracao = request.form.get('duracao')

    nova_tarefa = Tarefa(tarefa=tarefa, descricao=descricao, duracao=duracao)
    db.session.add(nova_tarefa)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco de dados e as tabelas
    app.run(debug=True)