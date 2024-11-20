
from flask import Flask, render_template, request, redirect, flash, url_for
from link import DB  # 引入你的資料庫操作類別
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from crud import crud  # 導入 crud.py 中的藍圖
from api.sql import DB

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於會話加密

# 註冊藍圖
app.register_blueprint(crud, url_prefix='/crud')

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, email, username, permission ):
        self.id = id
        self.email = email
        self.username = username
        self.permission = permission




@login_manager.user_loader
def load_user(user_id):
    sql = "SELECT id, email, username, permission FROM userinformation WHERE id = %s"
    user = DB.fetchone(sql, (user_id,))
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

@app.route('/')
def index():
    return render_template('index.html')  # 顯示首頁

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT id, password, username, permission FROM userinformation WHERE email = %s"
        user_data = DB.fetchone(sql, (email,))

        if user_data and user_data[1] == password:  # 直接比較密碼
            user = User(user_data[0], email, user_data[2], user_data[3] )
            login_user(user)  # 登入用戶
            return redirect(url_for('dashboard'))  # 登入成功後重定向到儀表板

        flash('電子郵件或密碼錯誤，請再試一次')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        # 檢查是否已存在的電子郵件
        existing_user = DB.fetchone("SELECT id FROM userinformation WHERE email = %s", (email,))
        if existing_user:
            flash('此電子郵件已被註冊，請使用其他電子郵件。')
            return redirect(url_for('index'))  # 返回首頁

        # 將新用戶插入到資料庫
        DB.execute_input("INSERT INTO userinformation (username, email, password, permission) VALUES (%s, %s, %s, %s)", (username, email, password, 'user'))
        flash('註冊成功！請登入。')
        return redirect(url_for('login'))  # 註冊成功後重定向到登入頁面

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # 獲取書籍資料

    sql = "SELECT * FROM book_title;"  # 假設你的書籍資料表為 book_title
    books = DB.fetchall(sql)
    if current_user.permission != 'admin':
        
        return render_template('dashboard_user.html', books=books)
    else:

        return render_template('dashboard_admin.html', books=books)  # 將書籍資料傳遞給模板

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)  # 開啟 debug 模式
