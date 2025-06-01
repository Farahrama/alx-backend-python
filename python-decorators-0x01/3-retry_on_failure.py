import time
import sqlite3
import functools

# من التمرين السابق
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# decorator لإعادة المحاولة في حالة الفشل
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise  # فشل نهائي، نرمي الخطأ
                    print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# تجربة جلب البيانات
users = fetch_users_with_retry()
print(users)
