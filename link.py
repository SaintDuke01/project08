import psycopg2
from psycopg2 import pool
from flask_login import UserMixin

class DB:
    # 設置連接池
    connection_pool = pool.SimpleConnectionPool(
        1, 100,  # 最小和最大連線數
        user='project_8',
        password='p3gtkz',  # 請填入你的資料庫密碼
        host='140.117.68.66',      # 請填入你的資料庫主機
        port='5432',
        dbname='project_8'
    )

    @staticmethod
    def connect():
        return DB.connection_pool.getconn()

    @staticmethod
    def release(connection):
        DB.connection_pool.putconn(connection)

    @staticmethod
    def fetchall(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchone(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def execute(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                connection.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()  # 進行錯誤回滾
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def create_user(email, password):
        sql = 'INSERT INTO userinformation (email, password) VALUES (%s, %s)'
        try:
            DB.execute(sql, (email, password))
        except psycopg2.Error as e:
            print(f"Error inserting user: {e}")

    @staticmethod
    def get_user_by_email(email):
        sql = "SELECT id, password FROM userinformation WHERE email = %s"
        return DB.fetchone(sql, (email,))
    

