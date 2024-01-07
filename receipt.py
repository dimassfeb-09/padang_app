import os
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Image
from reportlab.lib import colors 
from reportlab.lib.pagesizes import B6
from reportlab.lib.styles import getSampleStyleSheet 
from mysql.connector import MySQLConnection

class Receipt():

    def __init__(self, connection) -> None:
        self.connection: MySQLConnection = connection
    
    def generate_receipt(self, order_id, products,pdf_file_path):
        table_data = [
            ["Order ID", "Product Name", "Quantity", "Price/Item (Rp)", "Total Price (Rp)"]
        ]
        
        total_price = 0
        for product in products:
            product_name, quantity, price = product
            total_price += quantity * price
            table_data.append([order_id, product_name, f"{quantity}x", f"Rp {price}",f"Rp {price*quantity}"])

        pdf = SimpleDocTemplate(pdf_file_path, pagesize=(400, 330)) 
        styles = getSampleStyleSheet() 


        logo = Image("static/images/logo.png", width=50, height=50)
        title_style = styles["Heading1"] 
        title_style.alignment = 1

        title = Paragraph("Warung Padang", title_style) 

        style = TableStyle( 
            [ 
                ("BOX", (0, 0), (-1, -1), 1, colors.black), 
                ("GRID", (0, 0), (4, 4), 1, colors.black), 
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black), 
                ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
            ] 
        ) 
        
        table_data.append(["Total", "", "", "", f"Rp {total_price}"])
        table = Table(table_data, style=style) 

        pdf.build([logo, title, table])


    def get_receipt_by_order_id(self, order_id: int):
        cursor = self.connection.cursor()
        
        query = """
            SELECT product.name, order_item.quantity, product.price
            FROM order_item
            JOIN product ON order_item.product_id = product.id
            WHERE order_item.order_id = %s"""

        cursor.execute(query, (str(order_id),))

        order_items = cursor.fetchall()

        products = [(name, quantity, price) for name, quantity, price in order_items]

        return products
