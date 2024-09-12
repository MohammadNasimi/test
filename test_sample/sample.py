
def divide(a,b):
    if b == 0:
        raise ZeroDivisionError("cant divide by zero ... ")
    return a/b


class Person:
    def __init__(self,first_name,last_name):
        self.first_name = first_name
        self.last_name = last_name
        
        
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def email(self):
        return f'{self.fullname()}@gmail.com'.replace(' ', '')
    
    