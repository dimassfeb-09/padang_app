from flask import flash, redirect, url_for
from mysql.connector import MySQLConnection

class Auth():
    def __init__(self, connection) -> None:
        self.connection: MySQLConnection = connection
    
    def login(self,email:str, password: str):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        return user
    
    def register(self,name: str,email:str, password: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            self.connection.commit()  
            
            flash('Register berhasil', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            self.connection.rollback()  
            flash('Register gagal', 'error')
            return 'Register gagal'
        finally:
            cursor.close()