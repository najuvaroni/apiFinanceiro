from main import db

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    receitas = db.relationship('Receita', backref='usuario', lazy=True)
    despesas = db.relationship('Despesa', backref='usuario', lazy=True)

class Receita(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

class Despesa(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
