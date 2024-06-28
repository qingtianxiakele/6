from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # 启用CORS，如果需要的话


# 连接到MySQL数据库
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # 替换为你的数据库用户名
            password='1234',  # 替换为你的数据库密码
            database='seafoodmarket',  # 替换为你的数据库名
        )
        return conn
    except Error as e:
        print(e)
        return None

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user_role = request.form.get('role', '')  # 使用get方法，如果没有提供role参数则返回空字符串
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    # 插入数据到数据库
    if user_role == 'admin':
        cursor.execute('SELECT * FROM manager WHERE managerID = %s AND password = %s', (username, password))
    elif user_role == "purchaser":
        cursor.execute('SELECT * FROM customer WHERE customerID = %s AND password = %s', (username, password))
    elif user_role == "wholesaler":
        cursor.execute('SELECT * FROM saler WHERE salerID = %s AND password = %s', (username, password))
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return redirect('/login')  # 假设你有一个/login路由处理登录逻辑

if __name__ == '__main__':
    app.run(debug=True)