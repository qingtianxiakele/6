from flask import Flask, request, jsonify, session
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

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


# 登录逻辑
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_role = request.form.get('role', '')  # 使用get方法，如果没有提供role参数则返回空字符串
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    # 根据用户角色执行不同的查询逻辑，这里只是一个示例
    if user_role == 'admin':
        cursor.execute('SELECT * FROM manager WHERE managerID = %s AND password = %s', (username, password))
    elif user_role =="purchaser":
        cursor.execute('SELECT * FROM customer WHERE customerID = %s AND password = %s', (username, password))
    elif user_role =="wholesaler":
        cursor.execute('SELECT * FROM saler WHERE salerID = %s AND password = %s', (username, password))
    user = cursor.fetchone()

    if user:
        conn.close()
        return jsonify({"message": "登录成功"}), 200
    else:
        conn.close()
        return jsonify({"error": "账号或密码错误"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
