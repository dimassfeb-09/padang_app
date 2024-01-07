
from flask import Request

class Users():
    
    def __init__(self, request: Request) -> None:
        self.request = request
    
    def get_cookie_user_id(self):
        user_id = self.request.cookies.get("TOKEN-ID")
        return user_id
    
    def check_user_is_login(self):
        user = self.get_cookie_user_id()
        if user:
            return user
        else:
            return False
        