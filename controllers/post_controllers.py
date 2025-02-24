from ..models import Post, User
from ..app_config import db
from flask import request, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timezone
from flask_restx import Resource, Namespace, fields


posts_ns = Namespace('Posts', description='Manutenção de postagens')


post_model = posts_ns.model('PostModel', {
    'post_id': fields.Integer(description='ID da postagem'),
    'user_id': fields.Integer(description='ID do usuário que criou a postagem', required=True),
    'post_content': fields.String(description='Conteúdo da postagem', required=True),
    'created_at': fields.DateTime(description='Data e hora de criação da postagem'),
    'updated_at': fields.DateTime(description='Data e hora da última atualização da postagem'),
    'user': fields.String(description='Nome de usuário do autor da postagem')
})


@posts_ns.route('/new-post')
class PostCreateController(Resource):

    @posts_ns.expect(post_model)
    @posts_ns.response(201, 'Postagem criada com sucesso')
    @posts_ns.response(400, 'Conteúdo da postagem não fornecido')
    @login_required
    def post(self):
        post_data = request.json

        if not post_data.get('post_content'):
            return ({"message": "Adicione conteúdo para fazer a postagem!"}), 400
        
        new_post = Post(
            user_id=current_user.user_id,
            post_content=post_data['post_content'],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(new_post)
        db.session.commit()

        return ({"message": "Postagem feita :)", "post": new_post.to_dict()}), 201


@posts_ns.route('/all-posts')
class AllPostsController(Resource):
    
    @posts_ns.response(200, 'Lista de todas as postagens')
    @posts_ns.response(404, 'Não há postagens cadastradas')
    @login_required
    def get(self):
        posts = Post.query.all()

        if not posts:
            return ({"message": "Não há postagens cadastradas :("}), 404

        return ({"posts": [post.to_dict() for post in posts]}), 200


@posts_ns.route('/user/<string:username>')
class PostsByUserController(Resource):

    @posts_ns.param('username', 'Nome de usuário')
    @posts_ns.response(200, 'Lista de postagens do usuário')
    @posts_ns.response(404, 'Usuário não encontrado ou sem postagens')
    def get(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            return ({"message": "Usuário não encontrado :("}), 404

        posts = Post.query.filter_by(user_id=user.user_id).all()

        if not posts:
            return ({"message": f"{username} ainda não criou nenhuma postagem"}), 404

        return ({"posts": [post.to_dict() for post in posts]}), 200


@posts_ns.route('/my-posts')
class MyPostsController(Resource):

    @posts_ns.response(200, 'Lista de postagens do usuário logado')
    @posts_ns.response(404, 'Usuário logado não criou postagens')
    @login_required
    def get(self):
        posts = Post.query.filter_by(user_id=current_user.user_id).all()

        if not posts:
            return ({"message": "Você ainda não criou nenhuma postagem"}), 404

        return ({"posts": [post.to_dict() for post in posts]}), 200


@posts_ns.route('/post/<int:post_id>')
class PostByIdController(Resource):

    @posts_ns.response(200, 'Postagem encontrada')
    @posts_ns.response(404, 'Postagem não encontrada')
    @login_required
    def get(self, post_id):
        post = Post.query.get(post_id)

        if not post:
            return ({"message": "Postagem não encontrada :("}), 404

        return ({"post": post.to_dict()}), 200


    @posts_ns.response(200, 'Postagem atualizada com sucesso')
    @posts_ns.response(404, 'Postagem não encontrada')
    @posts_ns.response(403, 'Você não tem permissão para editar esse post')
    @posts_ns.expect(post_model)
    @login_required
    def put(self, post_id):
        post = Post.query.get(post_id)

        if not post:
            return ({"message": "Postagem não encontrada :("}), 404
        
        if post.user_id != current_user.user_id and not current_user.is_admin:
            return ({"message": "Você não tem permissão para editar essa postagem"}), 403
        
        post_data = request.json

        if 'post_content' in post_data:
            post.post_content = post_data['post_content']
            post.updated_at = datetime.now(timezone.utc)

        try:
            db.session.commit()
            return ({"message": "Postagem atualizada com sucesso :)", "post": post.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return ({"message": "Erro ao atualizar a postagem", "error": str(e)}), 500


    @posts_ns.response(200, 'Postagem deletada com sucesso')
    @posts_ns.response(404, 'Postagem não encontrada')
    @posts_ns.response(403, 'Você não tem permissão para deletar esse post')
    @login_required
    def delete(self, post_id):
        post = Post.query.get(post_id)

        if not post:
            return ({"message": "Postagem não encontrada :("}), 404

        if post.user_id != current_user.user_id and not current_user.is_admin:
            return ({"message": "Você não tem permissão para deletar essa postagem"}), 403

        try:
            db.session.delete(post)
            db.session.commit()
            return ({"message": "Postagem deletada com sucesso."}), 200
        except Exception as e:
            db.session.rollback()
            return ({"message": "Erro ao deletar a postagem.", "error": str(e)}), 500