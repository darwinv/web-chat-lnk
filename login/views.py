from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import Login


def weblogin(request):
    """
    Vista para mostrar el formulario de login y autenticar al usuario

    :param request:
    :return: formulario de login o listado de especialistas
    """
    error_message = ''
    
    if request.user.is_authenticated():
        return HttpResponseRedirect('/admin/actor/specialists')
    
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            # Autenticamos datos de usuario del backend
            
            user = authenticate(request, username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)

                # redirect according to user type
                return HttpResponseRedirect('/admin/actor/specialists')
            else:
                error_message = _("Wrong Credentials")
    else:
        form = Login()

    return render(request, 'public/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))
