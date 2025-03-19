from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    duracao = db.Column(db.Integer, nullable=False)  # em segundos
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_limite = db.Column(db.DateTime, nullable=False)
    progresso = db.Column(db.Float, default=0.0)
    expirada = db.Column(db.Boolean, default=False)

    def to_dict(self):
        agora = datetime.utcnow()
        tempo_total = (self.data_limite - self.data_criacao).total_seconds()
        tempo_passado = (agora - self.data_criacao).total_seconds()
        progresso = min((tempo_passado / tempo_total) * 100, 100) if tempo_total > 0 else 100
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'duracao': self.duracao // 60,  # Converter segundos para minutos
            'dataCriacao': self.data_criacao.timestamp() * 1000,
            'dataLimite': self.data_limite.timestamp() * 1000,
            'progresso': progresso,
            'expirada': self.expirada or agora >= self.data_limite
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    agora = datetime.utcnow()
    tarefas = Tarefa.query.all()
    for tarefa in tarefas:
        if not tarefa.expirada and agora >= tarefa.data_limite:
            tarefa.expirada = True
    db.session.commit()
    return jsonify([tarefa.to_dict() for tarefa in tarefas])

@app.route('/tarefas', methods=['POST'])
def add_tarefa():
    data = request.json
    nova_tarefa = Tarefa(
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        duracao=int(data['duracao']) * 60,
        data_criacao=datetime.utcnow(),
        data_limite=datetime.utcnow() + timedelta(minutes=int(data['duracao']))
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    return jsonify(nova_tarefa.to_dict()), 201

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'message': 'Tarefa removida'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

