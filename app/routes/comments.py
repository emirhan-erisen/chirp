from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment, Post

comments_bp = Blueprint("comments_bp", __name__)

@comments_bp.route("/", methods=["POST"])
@jwt_required()
def add_comment():
    data = request.get_json()
    content = data.get("content")
    post_id = data.get("post_id")
    user_id = get_jwt_identity()

    if not content or not post_id:
        return jsonify({"msg": "Missing content or post_id"}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    comment = Comment(content=content, post_id=post_id, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Comment added"}), 201

@comments_bp.route("/<int:post_id>", methods=["GET"])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    result = [
        {
            "id": c.id,
            "content": c.content,
            "timestamp": c.timestamp.isoformat(),
            "author": c.author.username
        } for c in comments
    ]
    return jsonify(result), 200