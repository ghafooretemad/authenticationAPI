
class UserFilterDependency:
    def __init__(self, name:str='', email:str='', phone:str='', department:int = 0):
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department

class PermissionFilterDependency:
    def __init__(self, name:str=''):
        self.name = name
        