#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login, logout
from django.urls import reverse
#seguridad
from django.contrib.auth import authenticate, login

#api
from api.connection import api

#forms
from .forms import Login


def weblogin(request):
    """
    Vista para mostrar el formulario de login y autenticar al usuario

    :param request:
    :return: formulario de login o listado de especialistas
    """
    user = error_message = ''
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/admin/actor/specialists')
    
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            # Autenticamos datos de usuario del backend
            
            user = authenticate(request, username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)

                #TODO
                #redirect according to user type
                return HttpResponseRedirect('/admin/actor/specialists')
            else:
               error_message = _("Wrong Credentials")
    else:
        form = Login()

    return render(request, 'public/login.html', {'form': form,'error_message': error_message})



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))