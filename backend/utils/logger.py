from models import db
from models.operation_log import OperationLog

def add_operation_log(user_id, operation_type, operation_desc):
    """
    添加操作日志
    :param user_id: 操作用户ID
    :param operation_type: 操作类型
    :param operation_desc: 操作描述
    """
    try:
        log = OperationLog(
            user_id=user_id,
            operation_type=operation_type,
            operation_desc=operation_desc
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error adding operation log: {str(e)}")
        db.session.rollback() 