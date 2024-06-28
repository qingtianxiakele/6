from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

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

# Flask路由来获取商品列表
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT commodity_name, price, num ,picture FROM commodity')  # 确保SQL语句与您的数据库结构匹配
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        # 将查询结果转换为列表的商品对象
        products_list = [{'commodity_name': product[0], 'price': product[1], 'num': product[2],'picture': product[3]} for product in products]
        return jsonify(products_list)
    else:
        return jsonify({"error": "Database connection failed"}), 500

# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)