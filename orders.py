from flask import flash, redirect, url_for
from mysql.connector import MySQLConnection

class Orders():
    
    def __init__(self, connection) -> None:
        self.connection: MySQLConnection = connection
    
    def get_order_details(self, order_id):
        cursor = self.connection.cursor()

        query = f"SELECT * FROM orders WHERE id = {order_id};"
        cursor.execute(query)
        order_details = cursor.fetchone()

        query = f"SELECT * FROM order_item WHERE order_id = {order_id};"
        cursor.execute(query)
        order_items = cursor.fetchall()

        cursor.close()

        return order_details, order_items
    
    def get_order_user(self,user_id:int):
        query = f"""
            SELECT
                o.id AS order_id,
                o.order_date AS order_date,
                oi.product_id,
                p.name,
                p.price,
                p.img,
                oi.quantity,
                oi.subtotal
            FROM
                orders o
            JOIN
                order_item oi ON o.id = oi.order_id
            JOIN
                product p ON oi.product_id = p.id
            WHERE
                o.user_id = {user_id}
            ORDER BY o.id DESC;
        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        user_orders = {"user_id": user_id, "orders": []}
        
        current_order_id = 0
        current_order = {}
        
        for row in results:
            order_id = row[0]
            order_date = row[1]
            product_id = row[2]
            name = row[3]
            price = row[4]
            img = row[5]
            quantity = row[6]
            subtotal = row[7]
            
            if order_id != current_order_id:
                if current_order:
                    current_order["total"] = sum(item["subtotal"] for item in current_order["order_items"])
                    user_orders["orders"].append(current_order)
                current_order_id = order_id
                current_order = {"order_id": current_order_id, "created_at": order_date, "order_items": []}

            current_order["order_items"].append({
                "product_id": product_id,
                "name": name,
                "price": price,
                "img": img,
                "quantity": quantity,
                "subtotal": subtotal
            })

        
        cursor.close()
        return user_orders

    def add_order(self, user_id, cart_list):
        cursor = self.connection.cursor()
        
        try:
            insert_order_query = f"""
            INSERT INTO `orders` (user_id, order_date)
            VALUES ({user_id}, NOW());
            """
            cursor.execute(insert_order_query)
            
            cursor.execute("SELECT LAST_INSERT_ID() AS last_id;")
            result = cursor.fetchone()
            
            last_inserted_order_id = 0
            if result:
                last_inserted_order_id = result[0]
            
            for item in cart_list["cart_list"]:
                product_id = item["product_id"]
                quantity = item["quantity"]
                price = item["price"]
                subtotal = quantity * price

                insert_order_item_query = f"""
                INSERT INTO order_item (order_id, product_id, quantity, subtotal)
                VALUES ({last_inserted_order_id}, {product_id}, {quantity}, {subtotal});
                """
                cursor.execute(insert_order_item_query)
            
            query_remove_cart = f"DELETE FROM checkout WHERE user_id = {user_id}"
            cursor.execute(query_remove_cart)
            self.connection.commit()    
            cursor.close()
            flash('Order barang berhasil.', 'success')
            return redirect(url_for('orders'))
        except Exception as e:
            self.connection.rollback()  
            flash('Order barang gagal.', 'error')
            return redirect(url_for('cart'))
        finally:
            cursor.close()        
        
        
        