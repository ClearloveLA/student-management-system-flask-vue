from datetime import datetime
from . import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.String(20), primary_key=True)  # 修改为String类型
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer)
    class_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    enrollment_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) 