from ..models import User
from ..app_config import db
from flask import request, jsonify
from flask_login import current_user, login_required
from flask_restx import Resource, Namespace, fields


users_ns = Namespace('Users', description='Manutenção dos dados dos usuários')


user_model = users_ns.model('UserModel', {
    'user_id': fields.Integer(description='ID do usuário'),
    'user_email': fields.String(description='Email do usuário', required=True),
    'user_password': fields.String(description='Senha de usuário', required=True),
    'username': fields.String(description='Nome de usuário', required=True),
    'is_admin': fields.Boolean(description='Indicador de que o usuário é Administrador ou não', default=False)  
})


@users_ns.route('/')
class UserController(Resource):

    @users_ns.expect(user_model)
    @users_ns.response(201, "Usuário criado com sucesso :)", model=user_model)
    @users_ns.response(400, "Dados obrigatórios faltando", model=user_model)
    @users_ns.response(409, "Usuário já existe")
    def post(self):
        user_data = request.json

        if not user_data.get('user_email'):
            return ({'message': 'É obrigatório inserir um email'}), 400
        if not user_data.get('user_password'):
            return ({'message': 'É obrigatório inserir uma senha'}), 400
        if not user_data.get('username'):
            return ({'message': 'É obrigatório inserir um username'}), 400
        
        existing_user = User.query.filter_by(user_email=user_data.get('user_email')).first()
        if existing_user:
            return ({'message': 'Usuário já existe. Por favor, faça login.'}), 409

        existing_username = User.query.filter_by(username=user_data.get('username')).first()
        if existing_username:
            return ({'message': 'Esse username já está em uso :('}), 409

        new_user = User(user_email=user_data['user_email'], 
                user_password_hash=user_data['user_password'],
                username=user_data['username'],
                is_admin=user_data.get('is_admin', False))
        
        new_user.secure_password(user_data['user_password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return ({"message": "Usuário criado, bem-vindo(a) ao Postify! :)", "user": new_user.to_dict()}), 201


    @users_ns.response(200, "Lista de usuários", model=user_model)
    @users_ns.response(200, "Não há usuários cadastrados :(")
    @login_required
    def get(self):
        users = User.query.all()

        if not users:
            return jsonify({"message": "Não há usuários cadastrados :("}), 200
        
        users_list = [{'user_id': user.user_id, 'username': user.username,} for user in users]

        return jsonify({'users': users_list})
    

@users_ns.route('/<string:username>')
class UserByUsernameController(Resource):

    @users_ns.response(200, "Detalhes do usuário", model=user_model)
    @users_ns.response(404, "Usuário não encontrado :(")
    @login_required
    def get(self, username):
        searched_user = User.query.filter_by(username=username).first()

        if searched_user is None:
            return jsonify({'message': 'Usuário não encontrado :('}), 404
        
        return jsonify({'user_id': searched_user.user_id, 'username': searched_user.username})


    @users_ns.param('user_email', 'Endereço de email do usuário')
    @users_ns.param('user_password', 'Senha de usuário')
    @users_ns.param('username', 'Nome de usuário')
    @users_ns.response(200, "Usuário atualizado com sucesso :)", model=user_model)
    @users_ns.response(403, "Você não tem permissão para editar esse usuário.")
    @users_ns.response(404, "Usuário não encontrado :(")
    @users_ns.response(500, "Erro ao atualizar o usuário")
    @login_required
    def put(self, username):
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return ({"message": "Usuário não encontrado :("}), 404
        
        if not current_user.is_admin and current_user.username != username:
            return ({"message": "Você não tem permissão para editar esse usuário."}), 403

        user_data = request.json

        if user_data.get('user_email'):
            user.user_email = user_data['user_email']
        if user_data.get('user_password'):
            user.secure_password(user_data['user_password'])
        if user_data.get('username'):
            user.username = user_data['username']
        if 'is_admin' in user_data and current_user.is_admin:
            user.is_admin = user_data['is_admin']

        try:
            db.session.commit()
            
            updated_user = user.to_dict()

            print(updated_user)
            print(type(updated_user))

            return ({
                "message": "Usuário atualizado com sucesso :)",
                "user": updated_user
            }), 200
        
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar usuário: {e}")
            return ({
                "message": "Erro ao atualizar o usuário.",
                "error": str(e)
            }), 500


    @users_ns.response(200, "Usuário deletado com sucesso", model=user_model)
    @users_ns.response(403, "Você não tem permissão para deletar esse usuário.")
    @users_ns.response(404, "Usuário não encontrado :(")
    @users_ns.response(500, "Erro ao deletar o usuário")
    @login_required
    def delete(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            return ({"message": "Usuário não encontrado :("}), 404
        
        if not current_user.is_admin and current_user.username != username:
            return ({"message": "Você não tem permissão para deletar esse usuário."}), 403

        try:
            user_name = user.username
            db.session.delete(user)
            db.session.commit()

            return ({
                "message": f"Usuário '{user_name}' deletado com sucesso.",
                "status": "success"
            }), 200
        
        except Exception as e:
            db.session.rollback()
            return ({
                "message": "Erro ao deletar o usuário.",
                "error": str(e)
            }), 500