from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
#from link import DB  # 引入你的資料庫操作類別
from api.sql import DB
#import app
from flask_login import UserMixin
import datetime

#把link.py 裡面的DB 實體化 ，然後調用裡面的function

crud = Blueprint('crud', __name__)

#管理者權限
#新增使用者
@crud.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.permission != 'admin':
        flash('你沒有權限執行此操作！')
        return redirect(url_for('crud.view_users'))

    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    existing_user = DB.fetchone("SELECT id FROM userinformation WHERE email = %s", (email,))
    if existing_user:
        flash('此電子郵件已被註冊，請使用其他電子郵件。')
        return redirect(url_for('crud.view_users'))

    try:
        DB.execute_input("INSERT INTO userinformation (email, password, permission) VALUES (%s, %s, %s)", (email, password, role))
        flash('使用者註冊成功！')
    except Exception as e:
        flash(f'新增使用者失敗: {e}')
    
    return redirect(url_for('crud.view_users'))

#管理者權限
# 查看所有使用者
@crud.route('/users', methods=['GET'])
@login_required
def view_users():
    # 更新 SQL 查詢，加入姓名 (username)
    users = DB.fetchall("SELECT id, email, permission, username FROM userinformation;")
    return render_template('users.html', users=users)

#管理者權限
# 刪除使用者
@crud.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.permission != 'admin':
        flash('你沒有權限執行此操作！')
        return redirect(url_for('crud.view_users'))

    try:
        DB.execute_input("DELETE FROM userinformation WHERE id = %s;", (user_id,))
        flash('使用者已刪除！')
    except Exception as e:
        flash(f'刪除使用者失敗: {e}')
    
    return redirect(url_for('crud.view_users'))

# 新增書籍
@crud.route('/add_book', methods=['POST'])
@login_required
def add_book():
    Callnumber = request.form['callnumber']
    content = request.form['content']
    name = request.form['name']
    author = request.form['author']

    try:
        # 將新書籍插入到資料庫
        DB.execute("INSERT INTO book_title (Callnumber, content, name, author) VALUES (%s, %s, %s, %s)", (Callnumber, content, name, author))
        flash('書籍新增成功！')
    except Exception as e:
        flash(f'新增書籍失敗: {e}')
    
    return redirect(url_for('crud.view_books'))

# 查看書籍
@crud.route('/books', methods=['GET'])
@login_required
def view_books():
    books = DB.fetchall("SELECT Callnumber, content, name, author FROM book_title;")
    return render_template('books.html', books=books)  # 將 books 變數傳遞給模板

#借閱書籍
@crud.route('/borrow_books', methods=['POST'])
@login_required
def borrow_books():
    # 從表單中獲取所有選中的書籍號碼
    selected_books = request.form.getlist('book_contents')
    
    # 檢查是否有選取的書籍
    if selected_books:
        # 處理選取的書籍號碼列表，進行借書操作
        for book_id in selected_books:
            # 使用參數化查詢來獲取書籍的資料
            book = DB.fetchall(f"SELECT bid.book_id, bid.serialnumber FROM book_id AS bid NATURAL JOIN book_title AS bt WHERE bt.callnumber = '{book_id}'")
            
            if book:
                book_id = book[0][0]  # 確認獲取正確的索引
                serialnumber = book[0][1]

                # 獲取當前時間並格式化
                current_time = datetime.datetime.now()
                borrowdatetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
                # 插入借書日誌
                DB.execute_input("INSERT INTO borrow_log (borrowdatetime, id, book_id, serialnumber) VALUES (%s, %s, %s, %s)", 
                 (borrowdatetime, current_user.id, book_id, serialnumber))

    flash('書籍借閱成功！')
    flash(selected_books)
    return render_template('borrow_result.html')

#借書車
@crud.route('/book_cart', methods=['POST'])
@login_required
def book_cart():
    # 從表單中獲取所有選中的書籍號碼
    selected_books = request.form.getlist('selected_books')
    books=[]
    # 檢查是否有選取的書籍
    if selected_books:
        # 處理選取的書籍號碼列表，進行借書操作
        for book_id in selected_books:
            # 使用參數化查詢來獲取書籍的資料
            book = DB.fetchall(f"SELECT bt.callnumber, bt.content, bt.name, bt.author FROM book_id AS bid NATURAL JOIN book_title AS bt WHERE bt.callnumber = '{book_id}'")
            books.append(book)



    return render_template('books_cart.html', books=books)

# 刪除書籍
@crud.route('/delete_book/<string:Callnumber>', methods=['POST'])
@login_required
def delete_book(Callnumber):
    try:
        DB.execute("DELETE FROM book_title WHERE Callnumber = %s;", (Callnumber,))
        flash('書籍已刪除！')
    except Exception as e:
        flash(f'刪除書籍失敗: {e}')
    
    return redirect(url_for('crud.view_books'))

# 查看書評
@crud.route('/book_reviews', methods=['GET'])
@login_required
def view_book_reviews():
    query = """
    SELECT b.Callnumber, b.name, br.description, br.score, u.email 
    FROM book_title b
    LEFT JOIN book_review br ON b.Callnumber = br.Callnumber
    LEFT JOIN userinformation u ON br.ID = u.id;  -- 確保你有把使用者的 email 加進來
    """
    reviews = DB.fetchall(query)

    # 查詢所有書籍以供下拉選單使用
    all_books_query = "SELECT Callnumber, name FROM book_title;"
    books = DB.fetchall(all_books_query)

    return render_template('book_reviews.html', reviews=reviews, books=books)


# 寫書評
@crud.route('/add_review', methods=['POST'])
@login_required
def add_review():
    callnumber = request.form['callnumber']  # 從表單中獲取書籍號碼
    description = request.form['description']
    score = request.form['score']
    
    try:
        DB.execute_input("INSERT INTO book_review (Callnumber, description, score, ID) VALUES (%s, %s, %s, %s)", 
                   (callnumber, description, score, current_user.id))
        flash('書評新增成功！')  # 添加成功訊息
    except Exception as e:
        flash(f'新增書評失敗: {e}')
    
    return redirect(url_for('crud.view_book_reviews'))

# 刪除書評
@crud.route('/delete_review', methods=['POST'])
@login_required
def delete_review():
    description = request.form['description']  # 獲取書評內容
    sql = "DELETE FROM book_review WHERE description = %s"  # 簡化表名引用
    try:
        DB.execute_input(sql, (description,))  # 將 description 包裝為元組
        flash('書評已刪除！')
    except Exception as e:
        flash(f'刪除書評失敗: {e}')
    
    return redirect(url_for('crud.view_book_reviews'))


# 修改書評
@crud.route('/edit_review', methods=['POST'])
@login_required
def edit_review():
    callnumber = request.form['callnumber']
    old_description = request.form['description']  # 獲取原書評內容
    new_description = request.form['new_description']  # 獲取新書評內容
    score = request.form['score']

    try:
        DB.execute("UPDATE book_review SET description = %s, score = %s WHERE Callnumber = %s AND description = %s AND ID = %s;", 
                   (new_description, score, callnumber, old_description, current_user.id))
        flash('書評已更新！')
    except Exception as e:
        flash(f'更新書評失敗: {e}')
    
    return redirect(url_for('crud.view_book_reviews'))


# 查看所有借閱紀錄
@crud.route('/borrowed_records', methods=['GET'])
@login_required
def view_borrowed_records():
    query = """
    SELECT b.callnumber, b.name, bl.borrowdatetime, u.username
    FROM borrow_log bl 
    INNER JOIN userinformation u ON bl.sn = u.id 
    NATURAL JOIN book_title b;
    """
    records = DB.fetchall(query)
    return render_template('borrowed_records.html', records=records)

#查看書籍借閱紀錄
@crud.route('/borrowed_records_book',methods=['POST', 'GET'])
@login_required
def view_borrowed_records_book():
    query = """
    SELECT name
    FROM book_title;
    """
    records = DB.fetchall(query)
    return render_template('borrow_result_book.html', records=records)

@crud.route('/borrowed_records_specific_book',methods=['POST', 'GET'])
@login_required
def view_borrowed_records_specific_book():
    bookname = request.form['book']  # 從表單中獲取書籍名稱

    query = f"""
        SELECT bt.name, bt.author, bl.borrowdatetime, u.username
        FROM (book_title AS bt NATURAL JOIN borrow_log AS bl) NATURAL JOIN userinformation AS u
        WHERE bt.name = '{bookname}';
    """
    records = DB.fetchall(query)

    return render_template('borrow_result_specific_book.html', records=records)


#查看個人借書紀錄
@crud.route('/borrowed_records_person', methods=['GET'])
@login_required
def view_borrowed_records_person():

    query = f"""
        SELECT bl.borrowdatetime, bt.name, bt.author
        FROM borrow_log AS bl NATURAL JOIN book_title AS bt
        WHERE bl.id = '{current_user.id}'
    """
    records = DB.fetchall(query)
    return render_template('borrow_result_person.html', records=records)


#選擇查看紀錄項目
@crud.route('/borrow_log_selection', methods=['GET'])
@login_required
def borrow_log_selection():
    return render_template('borrow_log_selection.html')


# Admin 管理書評
@crud.route('/admin/book_reviews', methods=['GET'])
@login_required
def admin_view_book_reviews():
    if current_user.permission != 'admin':  # 檢查用戶是否是管理者
        flash('您沒有權限訪問此頁面。')
        return redirect(url_for('crud.view_books'))

    query = """
    SELECT b.Callnumber, b.name, br.description, br.score, u.username 
    FROM book_title b
    LEFT JOIN book_review br ON b.Callnumber = br.Callnumber
    LEFT JOIN userinformation u ON br.ID = u.id; 
    """
    reviews = DB.fetchall(query)

    return render_template('admin_book_reviews.html', reviews=reviews)




@crud.route('/book_counts', methods=['GET'])
@login_required
def book_counts():
    # 定義 SQL 查詢
    query = """
    SELECT 
        b.callnumber, 
        bt.name AS book_name,
        COUNT(bl.book_id) AS borrow_count
    FROM 
        borrow_log AS bl
    NATURAL JOIN book_title AS bt
    NATURAL JOIN book_id AS b
    GROUP BY 
        b.callnumber, bt.name;
    """
    
    try:
        # 執行查詢並獲取結果
        reviews = DB.fetchall(query)
        
        # 檢查返回數據是否為空
        if not reviews:
            flash("No borrow records found.", "warning")
        else:
            flash("Borrow records retrieved successfully.", "success")
    except Exception as e:
        # 捕獲錯誤並記錄
        flash(f"Error fetching borrow records: {e}", "danger")
        reviews = []
    
    # 渲染模板，將查詢結果傳遞給前端
    return render_template('book_counts.html', reviews=reviews)





