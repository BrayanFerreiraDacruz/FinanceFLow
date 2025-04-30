from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)

    saldo_informado = db.Column(db.Float, default=0.0)
    despesas_informadas = db.Column(db.Float, default=0.0)

    transacoes = db.relationship('Transacao', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Transacao(db.Model):
    __tablename__ = 'transacao'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # 'receita' ou 'despesa'
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transacao {self.tipo} - R${self.valor:.2f}>'
