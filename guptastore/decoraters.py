from django.http import HttpRequest , HttpResponse
from django.shortcuts import redirect

def unauthenticatedUser(view_func):
    def wrapperFunc(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapperFunc


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapperFunc(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,*kwargs)
            else:
                return HttpResponse('ooo hacker')
            return view_func(request,*args,**kwargs)
        return wrapperFunc
    return decorator

def admin_only(view_func):
    def wrapperFunc(request,*args,**kwargs):
        group = None
        
        if request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        else :
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                # print('Groups = {} '.format(group))
                if group == 'customer':
                    return redirect('/')
            else :
                return redirect('login')
    return wrapperFunc
