from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class StaffAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).read_list(object_list, bundle)

    def read_detail(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).read_detail(object_list, bundle)
        
    def create_list(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).create_list(object_list, bundle)

    def create_detail(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).create_detail(object_list, bundle)

    def update_list(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).update_list(object_list, bundle)

    def update_detail(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).update_detail(object_list, bundle)

    def delete_list(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).delete_list(object_list, bundle)

    def delete_detail(self, object_list, bundle):
        user = bundle.request.user
        if not user.is_staff:
            raise Unauthorized("")
        else:
            super(StaffAuthorization,self).delete_detail(object_list, bundle)
