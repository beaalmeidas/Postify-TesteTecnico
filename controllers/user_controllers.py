from ..models import User
from ..run_app import app
from ..app_config import db
from flask import request, jsonify


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    new_user = User(user_email=user_data['user_email'], 
                    user_password_hash=user_data['user_password_hash'],
                    username=user_data['username'],
                    is_admin=user_data['is_admin'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso :)", "user": new_user.to_dict()}), 201


@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username,} for user in users]

    return jsonify({'users': users_list})


@app.route('users/<int:id>', methods=['GET'])
def get_user(id):
    searched_user = User.query.get(id)

    if searched_user is None:
        return jsonify({'message': 'Usuário não encontrado :('}), 404
    
    return jsonify({'id': searched_user.id, 'username': searched_user.username})