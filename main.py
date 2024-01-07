import os
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,make_response,send_from_directory
import mysql.connector
from http import cookies
from orders import Orders

from product import Product
from db import DB
from receipt import Receipt
from users import Users
from auth import Auth


app = Flask(__name__)
app.secret_key = "asdaisdtyqt2yet127gdhsbdas"

db = DB()
product = Product(connection=db.connection)
order = Orders(connection=db.connection)
receipt = Receipt(connection=db.connection)
auth = Auth(connection=db.connection)
users = Users(request=request)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == "POST":
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('TOKEN-ID')
        return response
    return render_template('index.html')            

@app.route('/', methods=['GET', 'POST'])
def home():
    products = product.get_product()
    user_id = request.cookies.get('TOKEN-ID')
    
    if not user_id:
        return render_template('login.html')
    
    users = {"id": user_id}
    
    return render_template('index.html', products=products, users=users)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    
    user_id = users.check_user_is_login()
    if user_id:
        order_list = order.get_order_user(int(user_id))
        return render_template('orders.html', orders=order_list)
    else:
        return redirect(url_for('login'))
    
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order_details, order_items = order.get_order_details(order_id)

    if order_details:
        response = {
            'order_id': order_details[0],
            'user_id': order_details[1],
            'order_date': order_details[2],
            'order_items': [
                {
                    'order_item_id': item[0],
                    'order_id': item[1],
                    'product_id': item[2],
                    'quantity': item[3],
                    'subtotal': item[4]
                }
                for item in order_items
            ]
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Order not found'}), 404

@app.route('/add_order', methods=['POST'])
def add_order():
        
    if request.method == "POST":
        user_id = users.get_cookie_user_id()
        cart_list = []
        if user_id:
            cart_list = product.get_cart_by_user_id(int(user_id))
            
        return order.add_order(user_id, cart_list)
    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    
    user_id = users.check_user_is_login()
    if user_id:
        cart_list = product.get_cart_by_user_id(int(user_id))
        return render_template('cart.html', carts=cart_list)
        
    return render_template('login.html')

@app.route('/add_cart', methods=['POST'])
def add_cart():
    try:
        
        product_id = request.form.get('product_id')
        user_id = request.form.get('user_id')

        if not product_id or not user_id:
            return jsonify({'error': 'Both product_id and user_id are required'}), 400

        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM checkout WHERE product_id = %s AND user_id = %s", (product_id, user_id))
        checkout = cursor.fetchone()
        
        if checkout:
            query = "UPDATE checkout SET quantity = quantity + 1 WHERE product_id = %s AND user_id = %s"
            cursor.execute(query, (product_id, user_id))
        else:
            query = "INSERT INTO checkout (product_id, user_id, quantity) VALUES (%s, %s, 1)"
            cursor.execute(query, (product_id, user_id))
                    
        db.connection.commit()
        cursor.close()

        flash('Berhasil tambah barang', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        db.connection.rollback()  
        flash(str(e), 'error')
        return redirect(url_for('home'))

@app.route('/get_receipt/<int:order_id>', methods=['GET'])
def get_receipt(order_id):
    print(order_id)
    data = receipt.get_receipt_by_order_id(order_id)
    if data:
        pdf_directory = "static/pdf"
        pdf_file_path = f"receipt_order_id_{order_id}.pdf"
        pdf_file_path = os.path.join(pdf_directory, pdf_file_path)

        # Ensure the directory exists
        os.makedirs(pdf_directory, exist_ok=True)

        receipt.generate_receipt(order_id, data, pdf_file_path)
        return send_from_directory(pdf_directory, f"receipt_order_id_{order_id}.pdf", as_attachment=True)
    else:
        return jsonify({
            "error": "Order ID not found"
        })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == "" or password == "":
            flash("Email dan password tidak boleh kosong", 'error')
            return redirect(url_for('login'))  
        
        user = auth.login(email, password)
        
        if not user:
            flash('Terjadi kesalahan: email atau password salah', 'error')
            return redirect(url_for('login'))  
        
        user_id = user[0]
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie("TOKEN-ID", str(user_id), max_age=604800)  
        resp.close()
        return resp
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if name == "" or email == "" or password == "": 
            flash("Nama, email dan password tidak boleh kosong", 'error')
            return redirect(url_for('register'))  

        return auth.register(name, email, password)

    return render_template('register.html')

@app.route('/remove_cart', methods=['POST'])
def remove_cart():
    try:
        cart_id = request.form.get('cart_id')
        query = f"DELETE FROM checkout WHERE id = {cart_id}"
        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        flash('Berhasil hapus dari cart.', 'success')
        return redirect(url_for('cart'))
    except Exception as e:
        db.connection.rollback()  
        flash(str(e), 'error')
        return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)