from tastypie.authentication import  BasicAuthentication

class StaffAuthentication(BasicAuthentication):
    def is_authenticated(self, request, **kwargs):
        check =  super(StaffAuthentication,self).is_authenticated(request, **kwargs)
        if check and request.user.is_staff:
            return True
        return False

    def get_identifier(self, request):
        return request.user.username
