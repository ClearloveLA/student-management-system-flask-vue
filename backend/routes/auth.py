from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User
from utils.logger import add_operation_log

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
        
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        password=hashed_password,
        email=email
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            
            # 记录登录日志
            add_operation_log(
                user.id,
                'LOGIN',
                f'用户登录: {username}'
            )
            
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'email': user.email
                },
                'message': '登录成功'
            }), 200
        return jsonify({'message': '用户名或密码错误'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': '登录失败'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user_id = get_jwt_identity()
    # 记录登出日志
    add_operation_log(
        current_user_id,
        'LOGOUT',
        '用户登出'
    )
    return jsonify({'message': '登出成功'}), 200