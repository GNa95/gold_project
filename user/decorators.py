from django.shortcuts import redirect
from .models import User

def login_required(func):
    def wrapper(request, *args, **kwargs):
        login_session = request.session.get('login_session','')

        if login_session == '':
            return redirect('/user/login/')
        
        return func(request, *args, **kwargs)
    return wrapper
    
# def test(func):

##########################
# context = {}
#   login_session = request.session.get('login_session', '')
#   if login_session == '':
#       context['login_session'] = False
#   else:
#       context['login_session'] = True
#   return render(request, 'main/index.html', context)