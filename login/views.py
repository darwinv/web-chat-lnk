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
        app = get_app_by_user(request.user.role.name)

        if app:
            return HttpResponseRedirect(reverse('{app}:index'.format(app=app)))
    
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            # Autenticamos datos de usuario del backend
            
            user = authenticate(request, username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)

                # redirect according to user type
                app = get_app_by_user(user.role.name)

                if app:
                    return HttpResponseRedirect(reverse('{app}:index'.format(app=app)))
            else:
                error_message = _("Wrong Credentials")
    else:
        form = Login()

    return render(request, 'public/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))


def get_app_by_user(role):
    """
    Funcion creada para retornar a que aplicacion debe redirigir cada rol de usuario
    :param role: String con le nombre del rol
    :return: nombre de la Django App Correspondiente al Rol
    """

    if role== 'admin':
        app = 'dashboard'
    elif role== 'client':
        app = 'client'
    elif role== 'specialist':
        app = 'specialist'
    elif role== 'seller':
        app = 'seller'
    else:
        app = None
        
    return app