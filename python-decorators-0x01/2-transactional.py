import sqlite3
import functools

# decorator لإدارة الاتصال بقاعدة البيانات
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# decorator لإدارة المعاملات (transactions)
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # العملية نجحت، نحفظ التغييرات
            return result
        except Exception as e:
            conn.rollback()  # حصل خطأ، نرجع التغييرات
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

# تجربة التحديث
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
