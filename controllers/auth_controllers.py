from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from ..models import User
from ..run_app import app


@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()

    if not login_data.get('email'):
        return jsonify({"message": "Insira seu email de usuário"}), 400
    if not login_data.get('password'):
        return jsonify({"message": "Insira sua senha de usuário"}), 400
    
    user = User.query.filter_by(user_email=login_data.get('email')).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado. Crie uma conta para entrar no Postify."}), 404

    if user and check_password_hash(user.user_password_hash, login_data.get('password')):
        login_user(user)
        return jsonify({"message": f"Bem-vindo(a), {user.username}!"}), 200

    return jsonify({"message": "Email ou senha inválidos"}), 401


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message:" "Saindo do Postify. Até a próxima!"}), 200


@app.route('/status', methods=['GET'])
@login_required
def status():
    admin_status = "Administrador" if current_user.is_admin else "Não-administrador"
    return jsonify({"message": f"Usuário atual: {current_user.username} - {admin_status}"}), 200