from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class StaffAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return object_list
        else:
            raise Unauthorized("")

    def read_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return True
        else:
            raise Unauthorized("")
        

    def create_list(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return object_list
        else:
            raise Unauthorized("")

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return True
        else:
            raise Unauthorized("")

    def update_list(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        allowed = []
        for obj in object_list:
            allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return True
        else:
            raise Unauthorized("")

    def delete_list(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return object_list
        else:
            raise Unauthorized("")

    def delete_detail(self, object_list, bundle):
        user = bundle.request.user
        if user.is_staff:
            return object_list
        else:
            raise Unauthorized("")
