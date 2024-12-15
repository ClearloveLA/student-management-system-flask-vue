from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    verify_jwt_in_request
)
from models import db
from models.student import Student
from sqlalchemy import or_
from datetime import datetime, timedelta
import random
from utils.logger import add_operation_log

student_bp = Blueprint('student', __name__)

# 生成模拟数据的函数
def generate_mock_data(count=520):
    # 删除现有数据
    Student.query.delete()
    
    # 班级列表
    class_names = [
        '应用22301班', '应用22302班', '应用22303班', '应用22304班', '应用22305班',
        '安全22301班', '安全22302班', '安全22303班', '安全22304班',
        '工软22301班', '工软22302班',
        '工网22301班'
    ]
    
    # 姓氏列表
    surnames = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    # 名字列表
    names = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
    
    students = []
    year = datetime.now().year
    
    for i in range(count):
        # 生成学号
        student_id = f"{year}{str(i+1).zfill(3)}"
        
        # 生成姓名
        name = random.choice(surnames)
        name += random.choice(names)
        if random.random() > 0.5:  # 50%概率生成三个字的名字
            name += random.choice(names)
            
        # 生成入学日期
        enrollment_date = datetime(year, 9, random.randint(1, 10))
        
        # 创建学生对象
        student = Student(
            id=student_id,
            name=name,
            gender=random.choice(['男', '女']),
            age=random.randint(18, 22),
            class_name=random.choice(class_names),
            phone=f"1{random.choice(['3','5','7','8','9'])}{str(random.randint(100000000, 999999999))}",
            email=f"student_{student_id}@example.com",
            address=f"第{random.randint(1,20)}省第{random.randint(1,20)}市第{random.randint(1,20)}区",
            enrollment_date=enrollment_date
        )
        students.append(student)
    
    # 批量保存到数据库
    db.session.bulk_save_objects(students)
    db.session.commit()
    return len(students)

# 添加生成数据的路由
@student_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_students():
    try:
        current_user_id = get_jwt_identity()
        count = generate_mock_data()
        
        # 记录生成数据日志
        add_operation_log(
            current_user_id,
            'GENERATE_DATA',
            f'生成{count}条模拟学生数据'
        )
        
        return jsonify({
            'message': f'成功生成{count}条学生数据',
            'count': count
        }), 201
    except Exception as e:
        print(f"Generate data error: {str(e)}")
        return jsonify({'message': '生成数据失败'}), 500

@student_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    try:
        # 打印认证信息
        current_user = get_jwt_identity()
        print(f"Current user ID: {current_user}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Authorization header: {request.headers.get('Authorization')}")
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        keyword = request.args.get('keyword', '')
        gender = request.args.get('gender', '')
        class_name = request.args.get('class_name', '')
        
        query = Student.query
        
        # 关键字搜索
        if keyword:
            query = query.filter(or_(
                Student.name.like(f'%{keyword}%'),
                Student.id.like(f'%{keyword}%'),
                Student.phone.like(f'%{keyword}%'),
                Student.class_name.like(f'%{keyword}%')
            ))
        
        # 性别筛选
        if gender:
            query = query.filter(Student.gender == gender)
        
        # 班级筛选
        if class_name:
            query = query.filter(Student.class_name == class_name)
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [{
                'id': s.id,
                'name': s.name,
                'gender': s.gender,
                'age': s.age,
                'class_name': s.class_name,
                'phone': s.phone,
                'email': s.email,
                'address': s.address,
                'enrollment_date': s.enrollment_date.strftime('%Y-%m-%d') if s.enrollment_date else None
            } for s in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        print(f"Error in get_students: {str(e)}")
        import traceback
        traceback.print_exc()  # 打印完整的错误堆栈
        return jsonify({'message': '获取学生列表失败', 'error': str(e)}), 500

@student_bp.route('/', methods=['POST'])
@jwt_required()
def add_student():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 生成学号：年份 + 3位序号
        year = datetime.now().year
        last_student = Student.query.filter(
            Student.id.like(f'{year}%')
        ).order_by(Student.id.desc()).first()
        
        if last_student:
            last_num = int(last_student.id[-3:])
            new_num = last_num + 1
        else:
            new_num = 1
            
        # 生成新学号
        student_id = f"{year}{str(new_num).zfill(3)}"
        
        # 检查学号是否已存在
        if Student.query.get(student_id):
            return jsonify({'message': '学号已存在'}), 400
        
        # 添加学号到数据
        data['id'] = student_id
        
        # 处理日期格式
        if 'enrollment_date' in data:
            data['enrollment_date'] = datetime.strptime(data['enrollment_date'], '%Y-%m-%d').date()
        
        new_student = Student(**data)
        db.session.add(new_student)
        db.session.commit()
        
        # 记录添加学生日志
        add_operation_log(
            current_user_id,
            'ADD_STUDENT',
            f'添加学生: {new_student.name}(学号:{new_student.id})'
        )
        
        return jsonify({
            'message': '添加成功',
            'id': new_student.id
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Add student error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': '添加失败', 'error': str(e)}), 500

@student_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(student, key):
            setattr(student, key, value)
    
    db.session.commit()
    return jsonify({'message': '更新成功'})

@student_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    try:
        current_user_id = get_jwt_identity()
        student = Student.query.get_or_404(id)
        
        # 记录删除学生日志
        add_operation_log(
            current_user_id,
            'DELETE_STUDENT',
            f'删除学生: {student.name}(学号:{student.id})'
        )
        
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        print(f"Delete student error: {str(e)}")
        return jsonify({'message': '删除失败'}), 500

@student_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        # 获取总人数
        total_students = Student.query.count()
        
        # 获取性别分布
        gender_stats = db.session.query(
            Student.gender,
            db.func.count(Student.id)
        ).group_by(Student.gender).all()
        
        # 获取专业分布（从班级名称中提取专业）
        class_stats = db.session.query(
            Student.class_name,
            db.func.count(Student.id)
        ).group_by(Student.class_name).all()
        
        # 按专业分组
        major_stats = {}
        for class_name, count in class_stats:
            # 从班级名称中提取专业名称（如 "应用22301班" -> "应用"）
            major = class_name[:2]  # 假设专业名都是2个字
            if major not in major_stats:
                major_stats[major] = 0
            major_stats[major] += count
        
        # 获取年龄分布
        age_stats = db.session.query(
            Student.age,
            db.func.count(Student.id)
        ).group_by(Student.age).all()
        
        return jsonify({
            'total_students': total_students,
            'gender_distribution': dict(gender_stats),
            'class_distribution': dict(class_stats),
            'major_distribution': major_stats,
            'age_distribution': dict(age_stats)
        })
    except Exception as e:
        print(f"Error in get_stats: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': '获取统计数据失败', 'error': str(e)}), 500 