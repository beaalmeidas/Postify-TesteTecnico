from flask import request
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from flask_restx import Resource, Namespace, fields


auth_ns = Namespace('Authentication', description='Funções de autenticação')


# SCHEMA PARA DADOS DE LOGIN
auth_model = auth_ns.model('AuthModel', {
    'email': fields.String(description='Email do usuário', required=True),
    'password': fields.String(description='Senha do usuário', required=True)
})


# SCHEMA PARA USUÁRIO LOGADO
status_model = auth_ns.model('StatusModel', {
    'message': fields.String(description='Mostra qual usuário está logado')
})


# FUNÇÃO LOGIN
@auth_ns.route('/login')
class LoginController(Resource):
    
    @auth_ns.expect(auth_model)
    @auth_ns.response(200, "Login bem-sucedido")
    @auth_ns.response(400, "Campos obrigatórios ausentes")
    @auth_ns.response(401, "Credenciais inválidas")
    @auth_ns.response(404, "Usuário não encontrado")
    def post(self):
        login_data = request.get_json()

        if not login_data.get('email'):
            return {"message": "Insira seu email de usuário"}, 400
        if not login_data.get('password'):
            return {"message": "Insira sua senha de usuário"}, 400
        
        user = User.query.filter_by(user_email=login_data.get('email')).first()

        if not user:
            return {"message": "Usuário não encontrado. Crie uma conta para entrar no Postify."}, 404

        if check_password_hash(user.user_password_hash, login_data.get('password')):
            login_user(user)
            return {"message": f"Bem-vindo(a), {user.username}!"}, 200

        return {"message": "Email ou senha inválidos"}, 401


# FUNÇÃO LOGOUT
@auth_ns.route('/logout')
class LogoutController(Resource):

    @auth_ns.response(200, "Logout realizado com sucesso")
    @login_required
    def post(self):
        logout_user()
        return {"message": "Saindo do Postify. Até a próxima!"}, 200


# FUNÇÃO DE CHECAR QUAL USUÁRIO ESTÁ LOGADO
@auth_ns.route('/status')
class StatusController(Resource):

    @auth_ns.response(200, "Status do usuário retornado")
    @auth_ns.marshal_with(status_model)
    @login_required
    def get(self):
        admin_status = "Administrador" if current_user.is_admin else "Não-administrador"
        return {"message": f"Usuário atual: {current_user.username} - {admin_status}"}, 200