import re

class User:

    def check_name(name):
        
        regex = "^[ A-Za-z]{3, }$"
        return re.fullmatch(regex, name)

    def check_uname(uname):

        regex = "^(?=.{4,20}$)+(?![_.])+(?!.*[_.]{2})+[a-zA-Z0-9._]+(?<![_.])*$"
        return re.fullmatch(regex, uname)
        
    def check_phone(phone):
        
        regex = "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        return re.fullmatch(regex, phone)

    def check_token_validity(token):

        regex = "^(?=.{4,20}$)+(?![_.])+(?!.*[_.]{2})+[a-zA-Z0-9._]+(?<![_.])\.[0-9a-f]{128}$"
        return re.fullmatch(regex, token)
    
    def check_email(email):

        regex = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        return re.fullmatch(regex, email)

    def __init__(self, uname:str,  name:str, email_ID:str, phone:int, access_token:str=None):
        

        if self.check_name(name):
            self.name = name
        else:
            raise Exception("Name not allowed, Regex not matched")
        
        if self.check_email(email_ID):
            self.email = email_ID
        else:
            raise Exception("Email not allowed, Regex not matched")

        if self.check_phone(phone):
            self.phone = phone
        else:
            raise Exception("Phone Number not allowed, Regex not matched")
        
        if self.check_uname(uname):
            self.uname = uname
        else:
            raise Exception("Username not allowed, Regex not matched")
        
        if self.check_token_validity(access_token) or (access_token == None):
            self.access_token = access_token
        else:
            raise Exception("Invalid Token format, Regex not matched")