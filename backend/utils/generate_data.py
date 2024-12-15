from faker import Faker
from models import db
from models.student import Student
import random
from datetime import datetime, timedelta

fake = Faker(['zh_CN'])  # 使用中文数据

def generate_students(count=520):
    """生成模拟学生数据"""
    students = []
    class_names = ['计算机科学1班', '计算机科学2班', '软件工程1班', '软件工程2班', 
                   '人工智能1班', '网络工程1班', '数据科学1班']


    # 生成学号前缀（如：2024）
    year = datetime.now().year
    
    for i in range(count):
        # 生成学号：年份 + 3位序号，例如：2024001
        student_id = f"{year}{str(i+1).zfill(3)}"
        
        # 随机生成入学日期
        enrollment_date = fake.date_between(
            start_date=f'{year}-09-01', 
            end_date=f'{year}-09-10'
        )
        
        student = Student(
            id=student_id,
            name=fake.name(),
            gender=random.choice(['男', '女']),
            age=random.randint(18, 22),
            class_name=random.choice(class_names),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            enrollment_date=enrollment_date
        )
        students.append(student)
    
    return students

def init_mock_data():
    """初始化模拟数据"""
    try:
        # 清空现有学生数据
        Student.query.delete()
        
        # 生成新的学生数据
        students = generate_students()
        db.session.bulk_save_objects(students)
        db.session.commit()
        
        return True, f"成功生成 {len(students)} 条学生数据"
    except Exception as e:
        db.session.rollback()
        return False, f"生成数据失败: {str(e)}" 