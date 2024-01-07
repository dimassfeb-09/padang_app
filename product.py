from mysql.connector import MySQLConnection

class Product():
    
    def __init__(self, connection) -> None:
        self.connection: MySQLConnection = connection
    
    def get_product(self):
        cursor = self.connection.cursor()
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

    def get_cart_by_user_id(self,user_id: int):
        query = f"""
                SELECT 
                    c.id AS cart_id,
                    c.product_id AS product_id,
                    p.name AS product_name,
                    p.price AS price,
                    p.img AS img,
                    c.quantity AS quantity
                FROM checkout AS c
                JOIN product AS p ON c.product_id = p.id
                WHERE c.user_id = {user_id};
                """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        products_db = cursor.fetchall()
        
        
        cart_list = []
        for row in products_db:
            product = {
                'cart_id': row[0],
                'product_id': row[1],
                'product_name': row[2],
                'price': row[3],
                'img': row[4],
                'quantity': row[5]
            }
            cart_list.append(product)
        
        cart_dict = {}
        item_totals = [item['quantity'] * item['price'] for item in cart_list]
        total_cost = sum(item_totals)
        
        cart_dict['total_price'] = total_cost
        cart_dict['cart_list'] = cart_list
        
            
        return cart_dict

    def get_order_by_user_id(self,user_id: int):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT
                o.order_date,
                o.id AS order_id,
                oi.id AS order_item_id,
                oi.product_id,
                oi.quantity,
                oi.subtotal,
                o.user_id
            FROM
                orders o
            JOIN
                order_item oi ON o.id = oi.order_id
        ''')

        rows = cursor.fetchall()

        orders_dict = {}
        for row in rows:
            order_date = row[0]
            order_id = row[1]
            order_item_id = row[2]
            product_id = row[3]
            quantity = row[4]
            subtotal = row[5]
            
            orders_dict["user_id"] = user_id
            
            
        
        return orders_dict

    def get_detail_product(self, product_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, name, price, img
            FROM product
            WHERE id = %s
        """, (product_id,))

        # Mengambil satu baris (satu produk)
        product = cursor.fetchone()

        # Menutup kursor dan koneksi
        cursor.close()

        # Jika produk tidak ditemukan, kembalikan None
        if not product:
            return None

        # Membuat dictionary berdasarkan hasil kueri
        result = {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "img": product[3]
        }

        return result
