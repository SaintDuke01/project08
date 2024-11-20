from typing import Optional
import psycopg2
from psycopg2 import pool


class DB:
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
    def execute_input(sql, input):
        if not isinstance(input, (tuple, list)):
            raise TypeError(f"Input should be a tuple or list, got: {type(input).__name__}")
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                connection.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def execute(sql):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

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


class Member:
    @staticmethod
    def get_member(account):
        sql = "SELECT account, password, mid, identity, name FROM userinformation WHERE account = %s"
        return DB.fetchall(sql, (account,))

    @staticmethod
    def get_all_account():
        sql = "SELECT account FROM userinformation"
        return DB.fetchall(sql)

    @staticmethod
    def create_member(input_data):
        sql = 'INSERT INTO userinformation (name, account, password, permission) VALUES (%s, %s, %s, %s)'
        DB.execute_input(sql, (input_data['name'], input_data['account'], input_data['password'], input_data['identity']))

    @staticmethod
    def delete_member(user_id):
        sql = 'DELETE FROM userinformation WHERE id = %s'
        DB.execute_input(sql, (user_id,))

    @staticmethod
    def get_role(userid):
        sql = 'SELECT permission, name FROM userinformation WHERE id = %s'
        return DB.fetchone(sql, (userid,))


class Product:
    @staticmethod
    def count():
        sql = 'SELECT COUNT(*) FROM book_title'
        return DB.fetchone(sql)

    @staticmethod
    def get_product(book_id):
        sql = 'SELECT * FROM book_title WHERE callnumber = %s'
        return DB.fetchone(sql, (book_id,))

    @staticmethod
    def get_all_product():
        sql = 'SELECT * FROM book_title'
        return DB.fetchall(sql)

    @staticmethod
    def add_product(input_data):
        sql = 'INSERT INTO book_title (callnumber, content, name, author) VALUES (%s, %s, %s, %s)'
        DB.execute_input(sql, (input_data['callnumber'], input_data['content'], input_data['name'], input_data['author']))

    @staticmethod
    def delete_product(callnumber):
        sql = 'DELETE FROM book_title WHERE callnumber = %s'
        DB.execute_input(sql, (callnumber,))

    @staticmethod
    def update_product(input_data):
        sql = 'UPDATE book_title SET content = %s, name = %s, author = %s WHERE callnumber = %s'
        DB.execute_input(sql, (input_data['content'], input_data['name'], input_data['author'], input_data['callnumber']))


class Record:
    @staticmethod
    def get_record(tno):
        sql = 'SELECT * FROM borrow_log WHERE tno = %s'
        return DB.fetchall(sql, (tno,))

    @staticmethod
    def add_record(input_data):
        sql = 'INSERT INTO borrow_log (BorrowDateTime, ID, Book_ID, SerialNumber) VALUES (%s, %s, %s, %s)'
        DB.execute_input(sql, (input_data['BorrowDateTime'], input_data['ID'], input_data['Book_ID'], input_data['SerialNumber']))


class Order_List:
    @staticmethod
    def add_order(input_data):
        sql = 'INSERT INTO order_list (mid, ordertime, price) VALUES (%s, %s, %s)'
        DB.execute_input(sql, (input_data['mid'], input_data['ordertime'], input_data['price']))

    @staticmethod
    def get_order():
        sql = '''
            SELECT o.oid, m.name, o.price, o.ordertime
            FROM order_list o
            NATURAL JOIN userinformation m
            ORDER BY o.ordertime DESC
        '''
        return DB.fetchall(sql)
