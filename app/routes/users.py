from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User

users_bp = Blueprint("users_bp", __name__)

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "followers": user.followers.count(),
        "following": user.followed.count()
    }), 200

@users_bp.route("/follow/<int:user_id>", methods=["POST"])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    current_user = User.query.get(current_user_id)
    if user == current_user:
        return jsonify({"msg": "You can't follow yourself."}), 400
    if user in current_user.followed:
        return jsonify({"msg": "Already following."}), 400
    current_user.followed.append(user)
    db.session.commit()
    return jsonify({"msg": f"Now following {user.username}"}), 200

@users_bp.route("/unfollow/<int:user_id>", methods=["POST"])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    current_user = User.query.get(current_user_id)
    if user not in current_user.followed:
        return jsonify({"msg": "Not following this user."}), 400
    current_user.followed.remove(user)
    db.session.commit()
    return jsonify({"msg": f"Unfollowed {user.username}"}), 200

@users_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    bio = data.get("bio")
    if bio:
        user.bio = bio
        db.session.commit()
        return jsonify({"msg": "Profile updated"}), 200
    return jsonify({"msg": "No changes provided"}), 400

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_own_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "followers": user.followers.count(),
        "following": user.followed.count()
    }), 200