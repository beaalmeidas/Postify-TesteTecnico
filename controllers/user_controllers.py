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


