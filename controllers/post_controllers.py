from ..models import Post, User
from ..run_app import app
from ..app_config import db
from flask import request, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timezone


@app.route('/posts', methods=['POST'])
@login_required
def create_post():
    post_data = request.json

    if not post_data.get('post_content'):
        return jsonify({"message": "Adicione conteúdo para fazer a postagem!"}), 400
    
    new_post = Post(
        user_id=current_user.user_id,
        post_content=post_data['post_content'],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Postagem feita :)", "post": new_post.to_dict()}), 201


# FUNÇÃO PARA MOSTRAR TODOS OS POSTS CADASTRADOS (QUALQUER USUÁRIO)
@app.route('/posts', methods=['GET'])
@login_required
def all_posts():
    posts = Post.query.all()

    if not posts:
        return jsonify({"message": "Não há postagens cadastradas :("}), 404

    return jsonify({"posts": [post.to_dict() for post in posts]}), 200


# FUNÇÃO PARA MOSTRAR TODOS OS POSTS DE UM USUÁRIO ESPECÍFICO
@app.route('/posts/user/<string:username>', methods=['GET'])
def get_posts_by_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado :("}), 404

    posts = Post.query.filter_by(user_id=user.user_id).all()

    if not posts:
        return jsonify({"message": f"{username} ainda não criou nenhuma postagem"}), 404

    return jsonify({"posts": [post.to_dict() for post in posts]}), 200


# FUNÇÃO PARA MOSTRAR TODOS OS POSTS DO USUÁRIO LOGADO
@app.route('/posts/me', methods=['GET'])
@login_required
def get_my_posts():
    posts = Post.query.filter_by(user_id=current_user.user_id).all()

    if not posts:
        return jsonify({"message": "Você ainda não criou nenhuma postagem"}), 404

    return jsonify({"posts": [post.to_dict() for post in posts]}), 200


# FUNÇÃO PARA OBTER UM POST ESPECÍFICO
@app.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"message": "Postagem não encontrada :("}), 404

    return jsonify({"post": post.to_dict()}), 200


@app.route('posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"message": "Postagem não encontrada :("}), 404
    
    if post.user_id != current_user.id and not current_user.is_admin:
        return jsonify({"message": "Você não tem permissão para editar essa postagem"}), 403
    
    post_data = request.json

    if 'post_content' in post_data:
        post.post_content = post_data['post_content']
        post.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return jsonify({"message": "Postagem atualizada com sucesso :)", "post": post.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar a postagem", "error": str(e)}), 500
    

@app.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"message": "Postagem não encontrada :("}), 404

    if post.user_id != current_user.user_id and not current_user.is_admin:
        return jsonify({"message": "Você não tem permissão para deletar essa postagem"}), 403

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Postagem deletada com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao deletar a postagem.", "error": str(e)}), 500