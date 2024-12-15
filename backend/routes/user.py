from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(f"Error in get_profile: {str(e)}")
        return jsonify({'message': '获取用户信息失败'}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return jsonify({'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        print(f"Error in update_profile: {str(e)}")
        return jsonify({'message': '更新失败'}), 500

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        if not check_password_hash(user.password, data.get('old_password')):
            return jsonify({'message': '旧密码错误'}), 400
        
        user.password = generate_password_hash(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
        print(f"Error in change_password: {str(e)}")
        return jsonify({'message': '密码修改失败'}), 500 