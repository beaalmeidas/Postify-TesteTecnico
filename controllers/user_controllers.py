from ..models import User
from ..app_config import db
from flask import request, jsonify
from flask_login import current_user, login_required
from flask_restx import Resource, Namespace, fields


api = Namespace('Users',description='Manutenção dados dos usuários')


user_model = api.model('UserModel', {
    'user_id': fields.Integer,
    'user_email': fields.String(description='User email', required=True),
    'user_password': fields.String(description='User password', required=True),
    'username': fields.String(description='Username', required=True),
    'is_admin': fields.Boolean(description='Flag indicating if the user has admin privileges', default=False)  
})


@api.route('/')
class UserController(Resource):

    @api.expect(user_model)
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


    @api.response(200, "Não há usuários cadastrados :(")
    @login_required
    def get():
        users = User.query.all()

        if not users:
            return jsonify({"message": "Não há usuários cadastrados :("}), 200
        
        users_list = [{'user_id': user.user_id, 'username': user.username,} for user in users]

        return jsonify({'users': users_list})
    

@api.route('/<string:username>')
class UserByUsernameController(Resource):

    @login_required
    def get(self, username):
        searched_user = User.query.get(username)

        if searched_user is None:
            return jsonify({'message': 'Usuário não encontrado :('}), 404
        
        return jsonify({'user_id': searched_user.user_id, 'username': searched_user.username})


@api.route('/<int:user_id>')
class UserByIdController(Resource):

    @api.response(200, "Teste update")
    @api.param('username','Nome de usuário')
    @api.param('email','Endereço de email do usuário')
    @api.param('password','Senha de usuário')
    @login_required
    def put(self, user_id):
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
    

    @api.response(200, "Deletando usuário")
    @login_required
    def delete(self, user_id):
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