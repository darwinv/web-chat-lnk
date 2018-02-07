from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import Login
from api.connection import api
from login.forms import RegisterClientFormNatural, RegisterClientFormBusiness
from dashboard.tools import ToolsBackend as Tools

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
    if 'token' in request.session:        
        obj_api = api()
        token = request.session['token']
        obj_api.logout(token)
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



def register(request):    
    obj_api = api()
    type_client = 'n'

    if 'type_client' in request.GET:
        type_client = request.GET['type_client']


    if request.method == 'POST':

        if type_client == 'n':
            # Crear formulario de registro para persona Natural
            form = RegisterClientFormNatural(data=request.POST, files=request.FILES, initial={'type_client': type_client})
            template = 'public/register_natural.html'
        else:
            # Crear formulario de registro para persona Juridica
            form = RegisterClientFormBusiness(data=request.POST, files=request.FILES, initial={'type_client': type_client})
            template = 'public/register_business.html'

        if form.is_valid():
            # Tomamos todo el formulario para enviarlo a la API
            data = form.cleaned_data
            data.update({
                "address": {
                    "street": data["street"],
                    "department": data["department"],
                    "province": data["province"],
                    "district": data["district"],
                }
            })

            data['username'] = data['email_exact']
            tools = Tools()

            if 'birthdate' in data:
                data['birthdate'] = tools.date_format_to_db(date=data['birthdate'])


            result = obj_api.post(slug='clients/', arg=data)

            if result and 'id' in result:
                if 'photo' in request.FILES:
                    photo = {'photo': request.FILES['photo']}
                    obj_api.put(slug='upload_photo/' + str(result['id']), files=photo)

                # Process success
                template = 'public/register_success.html'
            else:
                # Mostrar Errores en Form
                form.add_error_custom(add_errors=result)  # Agregamos errores retornados por la app para este formulario
            
    else:

        if type_client == 'n':
            # Crear formulario de registro para persona Natural
            form = RegisterClientFormNatural(initial={'type_client': type_client})
            template = 'public/register_natural.html'
        else:
            # Crear formulario de registro para persona Juridica
            form = RegisterClientFormBusiness(initial={'type_client': type_client})
            template = 'public/register_business.html'

    return render(request, template, {'form': form})
