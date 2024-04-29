from flask import Flask, jsonify, request, session
from main import app, db
from models import Usuario, Receita, Despesa
from flask_bcrypt import generate_password_hash, check_password_hash

@app.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    senha = data.get('senha')
    email = data.get('email')
    hashed_password = generate_password_hash(senha).decode('utf-8')
    new_user = Usuario(email=email, senha_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201


#retorna uma lista de todos os usuários cadastrados no sistema
@app.route('/usuarios', methods=['GET'])
def get_users():
    users = Usuario.query.all()
    result = []
    for user in users:
        result.append({'id_usuario': user.id_usuario, 'email': user.email})
    return jsonify({'usuarios': result}), 200

@app.route('/receitas', methods=['POST'])
def create_receita():
    if 'id_usuario' in session:
        data = request.json
        new_receita = Receita(descricao=data['descricao'], valor=data['valor'], usuario_id=session['id_usuario'])
        db.session.add(new_receita)
        db.session.commit()
        return jsonify({'mensagem': 'Receita criada com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

@app.route('/despesas', methods=['POST'])
def create_despesa():
    if 'id_usuario' in session:
        data = request.json
        new_despesa = Despesa(descricao=data['descricao'], valor=data['valor'], usuario_id=session['id_usuario'])
        db.session.add(new_despesa)
        db.session.commit()
        return jsonify({'mensagem': 'Despesa criada com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and check_password_hash(usuario.senha_hash, senha):
        if usuario and usuario.senha_hash == senha:
            session['id_usuario'] = usuario.id_usuario
            return jsonify({'mensagem': 'Login com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Email ou senha inválido'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'}), 200

@app.route('/receitas/<int:id_receita>', methods=['PUT'])
def update_receita(id_receita):
    if 'id_usuario' in session:
        data = request.json
        receita = Receita.query.filter_by(id_receita=id_receita, usuario_id=session['id_usuario']).first()
        if receita:
            receita.descricao = data.get('descricao', receita.descricao)
            receita.valor = data.get('valor', receita.valor)
            db.session.commit()
            return jsonify({'mensagem': 'Receita atualizada com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Receita não encontrada ou não autorizada'}), 404
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

@app.route('/receitas/<int:id_receita>', methods=['DELETE'])
def delete_receita(id_receita):
    if 'id_usuario' in session:
        receita = Receita.query.filter_by(id_receita=id_receita, usuario_id=session['id_usuario']).first()
        if receita:
            db.session.delete(receita)
            db.session.commit()
            return jsonify({'mensagem': 'Receita excluída com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Receita não encontrada ou não autorizada'}), 404
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

@app.route('/despesas/<int:id_despesa>', methods=['PUT'])
def update_despesa(id_despesa):
    if 'id_usuario' in session:
        data = request.json
        despesa = Despesa.query.filter_by(id_despesa=id_despesa, usuario_id=session['id_usuario']).first()
        if despesa:
            despesa.descricao = data.get('descricao', despesa.descricao)
            despesa.valor = data.get('valor', despesa.valor)
            db.session.commit()
            return jsonify({'mensagem': 'Despesa atualizada com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Despesa não encontrada ou não autorizada'}), 404
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

@app.route('/despesas/<int:id_despesa>', methods=['DELETE'])
def delete_despesa(id_despesa):
    if 'id_usuario' in session:
        despesa = Despesa.query.filter_by(id_despesa=id_despesa, usuario_id=session['id_usuario']).first()
        if despesa:
            db.session.delete(despesa)
            db.session.commit()
            return jsonify({'mensagem': 'Despesa excluída com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Despesa não encontrada ou não autorizada'}), 404
    else:
        return jsonify({'mensagem': 'Requer Autorização'}), 401

# Rota protegida que requer autenticação
@app.route('/protected', methods=['GET'])
def protected():
    # Verifica se o usuário está autenticado verificando se o email está na sessão
    if 'id_usuario' in session:
        return jsonify({'mensagem': 'Rota Protegida'})
    else:
        # Se o usuário não estiver autenticado, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Requer Autorização'})