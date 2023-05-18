from api.authApp.models import Profile, User


class UserFilterDependency:
    def __init__(self, name: str = '', email: str = '', phone: str = '', department: int = ''):
        self.params = [{"value": name, "model": Profile.first_name},
                       {"value": name, "model": Profile.last_name},
                       {"value": email, "model": User.email},
                       {"value": phone, "model": Profile.phone},
                       {"value": department, "model": User.department_id}]

    def prepareFilter(self):
        filterParams = list()
        for i in self.params:
            if(i["value"] != ''):
                filterParams.append(i["model"].contains(i["value"])) 

        return filterParams

class PermissionFilterDependency:
    def __init__(self, name: str = ''):
        self.name = name