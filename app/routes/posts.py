from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Post, User

posts_bp = Blueprint("posts_bp", __name__)

@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    if post.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted"}), 200

@posts_bp.route("/", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    content = data.get("content")
    user_id = get_jwt_identity()

    if not content:
        return jsonify({"msg": "Content is required"}), 400

    post = Post(content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"msg": "Post created successfully"}), 201

@posts_bp.route("/", methods=["GET"])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # sabit belirlenmiş gönderi sayısı

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    result = []
    for post in posts.items:
        result.append({
            "id": post.id,
            "content": post.content,
            "timestamp": post.timestamp.isoformat(),
            "author": post.author.username
        })
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": posts.total,
        "pages": posts.pages,
        "posts": result
    }), 200

@posts_bp.route("/feed", methods=["GET"])
@jwt_required()
def get_feed():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # sabit sayfa başı gönderi

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    followed_ids = [u.id for u in user.followed]

    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    result = []
    for post in posts.items:
        result.append({
            "id": post.id,
            "content": post.content,
            "timestamp": post.timestamp.isoformat(),
            "author": post.author.username
        })
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": posts.total,
        "pages": posts.pages,
        "posts": result
    }), 200

@posts_bp.route("/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    if post in user.liked_posts:
        return jsonify({"msg": "Already liked"}), 400

    user.liked_posts.append(post)
    db.session.commit()
    return jsonify({"msg": "Post liked"}), 200

@posts_bp.route("/<int:post_id>/unlike", methods=["POST"])
@jwt_required()
def unlike_post(post_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    if post not in user.liked_posts:
        return jsonify({"msg": "Not liked"}), 400

    user.liked_posts.remove(post)
    db.session.commit()
    return jsonify({"msg": "Post unliked"}), 200