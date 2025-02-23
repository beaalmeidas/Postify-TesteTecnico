from ..models import User
from ..run_app import app
from ..app_config import db
from flask import request, jsonify
from flask_login import current_user, login_required


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json

    if not user_data.get('email'):
        return jsonify({'message': 'É obrigatório inserir um email'}), 400
    if not user_data.get('password'):
        return jsonify({'message': 'É obrigatório inserir uma senha'}), 400
    if not user_data.get('username'):
        return jsonify({'message': 'É obrigatório inserir um username'}), 400
    
    existing_user = User.query.filter_by(user_email=user_data.get('email')).first()
    if existing_user:
        return jsonify({'message': 'Usuário já existe. Por favor, faça login.'}), 409

    existing_username = User.query.filter_by(username=user_data.get('username')).first()
    if existing_username:
        return jsonify({'message': 'Esse username já está em uso :('}), 409

    new_user = User(user_email=user_data['user_email'], 
                    user_password_hash=user_data['password'],
                    username=user_data['username'],
                    is_admin=user_data['is_admin', False])
    
    new_user.secure_password(user_data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado, bem-vindo(a) ao Postify! :)", "user": new_user.to_dict()}), 201


@app.route('/users', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()

    if not users:
        return jsonify({"message": "Não há usuários cadastrados :("}), 200
    
    users_list = [{'user_id': user.user_id, 'username': user.username,} for user in users]

    return jsonify({'users': users_list})


@app.route('users/<int:id>', methods=['GET'])
@login_required
def get_user(user_id):
    searched_user = User.query.get(user_id)

    if searched_user is None:
        return jsonify({'message': 'Usuário não encontrado :('}), 404
    
    return jsonify({'user_id': searched_user.user_id, 'username': searched_user.username})


@app.route('/users/<int:id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado :("}), 404
    
    if not current_user.is_admin and current_user.user_id != user_id:
        return jsonify({"message": "Você não tem permissão para editar esse usuário."}), 403

    user_data = request.json

    if user_data.get('username'):
        user.username = user_data['username']
    if user_data.get('email'):
        user.user_email = user_data['email']
    if user_data.get('password'):
        user.secure_password(user_data['password'])
    if 'is_admin' in user_data and current_user.is_admin:
        user.is_admin = user_data['is_admin']

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso :)", "user": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar o usuário.", "error": str(e)}), 500
    

@app.route('/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuário não encontrado :("}), 404
    
    if not current_user.is_admin and current_user.user_id != user_id:
        return jsonify({"message": "Você não tem permissão para deletar esse usuário."}), 403

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao deletar o usuário.", "error": str(e)}), 500