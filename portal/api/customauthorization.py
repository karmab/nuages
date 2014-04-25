from tastypie.authorization import Authorization

class StaffAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return object_list
        elif user.is_staff:
            return object_list
        else:
            return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return True
        elif user.is_staff:
            return True
        else:
            return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return True
        elif user.is_staff:
            return True
        else:
            return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return object_list
        elif user.is_staff:
            return object_list
        else:
            allowed = []
            for obj in object_list:
                if obj.user == bundle.request.user:
                    allowed.append(obj)
            return allowed

    def update_detail(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return True
        elif user.is_staff:
            return True
        else:
            return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return True
        elif user.is_staff:
            return True
        else:
            return bundle.obj.user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        user  = bundle.request.user
        if user.username == 'AnonymousUser':
            return object_list
        elif user.is_staff:
            return object_list
        else:
            allowed = []
            for obj in object_list:
                if obj.user == bundle.request.user:
                    allowed.append(obj)
            return allowed
