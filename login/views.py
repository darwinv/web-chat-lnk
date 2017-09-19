from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from api.connection import api
from django.utils.translation import ugettext_lazy as _

from .forms import Login

def login(request):
    user = ''
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            apiObj = api()
            user = apiObj.token(request.POST['user'],request.POST['password'])
            
            if 'access_token' in user:            
                return HttpResponseRedirect('/admin/')
            else:
                return render(request, 'public/login.html', {
                'error_message': _("Wrong Credentials"),'user': user
                })
    else:
        form = Login()

    return render(request, 'public/login.html', {'form': form})