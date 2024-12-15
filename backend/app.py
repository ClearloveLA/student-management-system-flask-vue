from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, 
    get_jwt_identity, 
    verify_jwt_in_request,
    jwt_required
)
from models import db
from flask_sqlalchemy import SQLAlchemy
from routes.auth import auth_bp
from routes.student import student_bp
from routes.user import user_bp
from routes.system import system_bp

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'wtc'
app.config['JWT_SECRET_KEY'] = 'wtc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/student_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60  # token有效期24小时
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'

# CORS配置
CORS(app, 
     resources={
         r"/api/*": {
             "origins": ["http://localhost:5173"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Authorization"],
             "supports_credentials": True,
             "max_age": 86400
         }
     })

# 禁用URL重定向
app.url_map.strict_slashes = False

jwt = JWTManager(app)
db.init_app(app)

# JWT错误处理
@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid token error: {error}")
    print(f"Request headers: {dict(request.headers)}")
    return jsonify({
        'message': f'Invalid token: {error}'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    print(f"Missing token error: {error}")
    print(f"Request headers: {dict(request.headers)}")
    return jsonify({
        'message': f'Missing token: {error}'
    }), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    print(f"Token expired. Header: {jwt_header}, Data: {jwt_data}")
    return jsonify({
        'message': 'Token has expired'
    }), 401

# 添加一个测试端点
@app.route('/api/v1/test-auth')
@jwt_required()
def test_auth():
    current_user = get_jwt_identity()
    return jsonify({
        'message': 'Authentication successful',
        'user_id': current_user
    })

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(student_bp, url_prefix='/api/v1/students')
app.register_blueprint(system_bp, url_prefix='/api/v1/system')
app.register_blueprint(user_bp, url_prefix='/api/v1/users')

@app.route('/')
def hello():
    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建所有数据库表
    app.run(debug=True, host='0.0.0.0', port=5000) 