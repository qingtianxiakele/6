from flask import Flask, request, jsonify
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


# Flask路由来添加商品
@app.route('/add_product', methods=['POST'])
def add_product():
    # 从请求中获取数据
    product_name = request.form.get('productName')
    product_price = request.form.get('productPrice')
    product_stock = request.form.get('productStock')
    product_describe = request.form.get('productdescribe')
    salerID = request.form.get('username')

    # 读取图片文件
    product_image_file = request.files.get('productImage')
    if product_image_file:
        product_image_path = 'path/to/save/' + product_image_file.filename
        product_image_file.save(product_image_path)

    # 连接数据库并添加商品记录
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO commodity (commodity_name, picture, price, num,describe,salerID) VALUES (%s, %s, %s, %s,%s,%s)',
            (product_name, product_image_path, product_price, product_stock, product_describe, salerID))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Product added successfully"}), 201
    else:
        return jsonify({"error": "Database connection failed"}), 500


# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
