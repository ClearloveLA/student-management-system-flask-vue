from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.operation_log import OperationLog
from datetime import datetime, timedelta
from utils.generate_data import init_mock_data

system_bp = Blueprint('system', __name__)

@system_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        operation_type = request.args.get('operation_type', '')
        
        # 构建查询
        query = db.session.query(
            OperationLog,
            User.username
        ).join(User)
        
        # 按操作类型筛选
        if operation_type:
            query = query.filter(OperationLog.operation_type == operation_type)
        
        # 按时间倒序排序
        query = query.order_by(OperationLog.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [{
                'id': log.OperationLog.id,
                'user_id': log.OperationLog.user_id,
                'username': log.username,
                'operation_type': log.OperationLog.operation_type,
                'operation_desc': log.OperationLog.operation_desc,
                'created_at': log.OperationLog.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for log in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        print(f"Error in get_logs: {str(e)}")
        return jsonify({'message': '获取日志失败'}), 500

@system_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    # 检查权限
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403
    
    # 获取系统基本统计信息
    total_users = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    normal_user_count = User.query.filter_by(role='user').count()
    
    # 获取最近的系统操作日志
    recent_logs = OperationLog.query.order_by(
        OperationLog.created_at.desc()
    ).limit(5).all()
    
    return jsonify({
        'user_stats': {
            'total_users': total_users,
            'admin_count': admin_count,
            'normal_user_count': normal_user_count
        },
        'recent_logs': [{
            'operation_type': log.operation_type,
            'operation_desc': log.operation_desc,
            'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for log in recent_logs]
    })

# 添加日志的辅助函数
def add_operation_log(user_id, operation_type, operation_desc):
    log = OperationLog(
        user_id=user_id,
        operation_type=operation_type,
        operation_desc=operation_desc
    )
    db.session.add(log)
    db.session.commit() 

# 添加生成模拟数据的路由
@system_bp.route('/mock/generate', methods=['POST'])
@jwt_required()
def generate_mock_data():
    # 检查权限
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403
    
    success, message = init_mock_data()
    
    # 记录操作日志
    add_operation_log(
        current_user.id,
        'GENERATE_MOCK_DATA',
        f'生成模拟数据: {message}'
    )
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 500 