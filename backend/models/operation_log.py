from datetime import datetime
from . import db

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    operation_type = db.Column(db.String(20))
    operation_desc = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联到用户
    user = db.relationship('User', backref='operation_logs')