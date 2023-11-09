from django.shortcuts import redirect
from django.http import JsonResponse

def login_check(func):
    def inner(request,*args,**kwargs):
        if 'ActiveUserEmail' not in request.session:
            response=redirect('app1:sign_in')
            response.set_cookie('msg_info',"You are not logged in...",5)
            return response
        return func(request,*args,**kwargs)
    return inner