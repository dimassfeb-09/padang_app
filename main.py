from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import mysql.connector

host = "localhost"
user = "root"
password = "Aa11bb22_"
database = "padang_app"

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

app = Flask(__name__)
app.secret_key = "asdaisdtyqt2yet127gdhsbdas"
    

def get_product():
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, price, img FROM product")
    
    products_db = cursor.fetchall()
    products = []
    for row in products_db:
        product = {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'img': row[3]
        }
        products.append(product)
            
    return products
   

@app.route('/', methods=['GET', 'POST'])
def home():
    products = get_product()
    return render_template('index.html', products=products)

@app.route('/add_cart', methods=['POST'])
def add_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        user_id = data.get('user_id')

        if not product_id or not user_id:
            return jsonify({'error': 'Both product_id and user_id are required'}), 400

        cur = connection.cursor()
        cur.execute("INSERT INTO checkout (product_id, user_id) VALUES (%s, %s)", (product_id, user_id))
        connection.commit()
        cur.close()

        return jsonify({'message': 'Product added to cart successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        
        if email == "" or password == "": 
            flash("Email dan password tidak boleh kosong", 'error')
            return redirect(url_for('login'))  
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        if user:
            return render_template('index.html')
        else:
            flash('Terjadi kesalahan: email atau password salah', 'error')
            return redirect(url_for('login'))  
        
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

        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            connection.commit()  
            
            flash('Register berhasil', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            connection.rollback()  
            flash('Register gagal', 'error')
            return 'Register gagal'
        finally:
            cursor.close()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)