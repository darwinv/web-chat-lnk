#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login

#seguridad
from django.contrib.auth import authenticate, login

#api
from api.connection import api

#forms
from .forms import Login


def weblogin(request):
    user = ''
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            print "form is_valid()"

            print request.POST['user']
            user = authenticate(request, username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)

                #TODO
                #redirect according to user type
                return HttpResponseRedirect('/admin/actor/specialists')
            else:
                return render(request, 'public/login.html', {
                'error_message': _("Wrong Credentials"),'user': user
                })
    else:
        form = Login()

    return render(request, 'public/login.html', {'form': form})