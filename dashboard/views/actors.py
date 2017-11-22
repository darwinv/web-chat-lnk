from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from api.connection import api

from dashboard.json2table import convert, getActualPage
from dashboard.forms import SpecialistForm, SellerFormFilters

import pdb


class Actor:
    logo_content_header = "fa fa-users"

    def generateHeader(self, custom_title=None):
        if custom_title:
            title = "{} - ".format(_("actors")).title() + custom_title
        else:
            title = self.title_content_header

        header = {'icon': self.logo_content_header, 'title': title}
        return {**header, **self.vars_page}


class Specialist(Actor):
    _list = 'dashboard:actor-specialists-list'
    _delete = 'dashboard:actor-specialists-delete'
    _detail = 'dashboard:actor-specialists-detail'
    _create = 'dashboard:actor-specialists-create'
    _edit = 'dashboard:actor-specialists-edit'
    vars_page = {
        'btn_specialists_class': 'active',
        'name_create_URL': _create,
    }

    @method_decorator(login_required)
    def list(self, request):
        ObjApi = api()
        filters = {}
        actual_page = getActualPage(request)
        arg = {"page": actual_page}
        token = request.session['token']
        title_page = _('specialists').title()

        # Filtro de especialista principal
        if 'main_specialist' in request.GET:
            main_specialist = request.GET['main_specialist']
            arg.update({"main_specialist": main_specialist})
            dataMainSpecilist = ObjApi.get(slug='specialists/' + main_specialist, token=token)
            filters.update({'main_specialist': dataMainSpecilist})
            title_page = _('associated specialists').title()


        # Traer data para el listado
        data = ObjApi.get(slug='specialists/', arg=arg, token=token)

        # Definimos columnas adicionales/personalizadas
        custom_column = {
            "last_name": {'type': 'concat', 'data': ('last_name', ' ', 'first_name')},
            "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}},
            "delete": {'type': 'delete', 'data': {'url': self._delete, 'key': 'id'}}
        }
        # Atributos para aplicar a la columna RUC
        attributes_colum = {
            "ruc":
                {
                    "class": "numeric"
                }
        }

        # Coloca los nombres de las cabeceras y a que columna van asociada, customColum tendra prioriedad
        lastnames_title = "{} {} {}".format(_("surnames"), _("and"), _("names"))

        header_tabla = [(_("detail"), "detail"),(lastnames_title, "last_name"),( _("code"), "code"),(
                        _("email"), "email_exact"),( _("RUC"), "ruc"),( _("category"), "category_name"),(
                        _("specialty"), "type_specialist_name"),( _("delete"), "delete")]

        tabla = convert(data, header=header_tabla, actual_page=actual_page, custom_column=custom_column,
                        attributes_colum=attributes_colum)

        # Titulo de la vista y variables de la Clase
        vars_page = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/specialistsList.html',
                      {'tabla': tabla, 'vars_page': vars_page, 'filters': filters})

    @method_decorator(login_required)
    def detail(self, request, id):
        ObjApi = api()
        data = ObjApi.get(slug='specialists/' + id, token=request.session['token'])

        # Si la data del usuario no es valida
        if type(data) is not dict or 'id' not in data:
            raise Http404()

        # Si esta definido el tipo de especialista que es el usuario
        if type(data) is dict and 'type_specialist' in data:
            type_specialist = data['type_specialist']
        else:
            type_specialist = ''

        # Titulo de la vista y variables de la Clase
        title_page = "{} {} - {}".format(_('specialist').title(), _(type_specialist), _('detail').title())
        vars_page = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/specialistsDetail.html', {'data': data, 'vars_page': vars_page})

    @method_decorator(login_required)
    def create(self, request):
        ObjApi = api()
        token = request.session['token']

        # Si llega envio por POST se valida contra el SpecialistForm
        if request.method == 'POST':
            form = self.generateFormSpecialist(data=request.POST, files=request.FILES)
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

                result = ObjApi.post(slug='specialists/', token=token, arg=data)

                if result and 'id' in result:

                    if 'photo' in request.FILES:
                        photo = {'photo': request.FILES['photo']}
                        ObjApi.put(slug='upload_photo/' + str(result['id']), token=token, files=photo)
                    # Process success
                    return HttpResponseRedirect(reverse(self._list))
                else:
                    # Mostrar Errores en Form
                    form.add_error_custom(
                        add_errors=result)  # Agregamos errores retornados por la app para este formulario

                    return render(request, 'admin/actor/specialistsForm.html', {'form': form})

        else:
            # Crear formulario de especialistas vacio, se traeran
            # datos de selecion como Categorias y Departamentos.
            form = self.generateFormSpecialist()

        title_page = _('create specialist').title()
        vars_page = self.generateHeader(custom_title=title_page)
        specialists_form = reverse(self._create)
        return render(request, 'admin/actor/specialistsForm.html',
                      {'vars_page': vars_page, 'form': form, 'specialists_form': specialists_form})

    def generateFormSpecialist(self, data=None, files=None, specilist=None, form_edit=None):
        """
        Funcion para generar traer formulario de especialistas

        :param data: objeto POST o dict de valores relacional
        :param specilist: dict que contiene los valores iniciales del usuario
        :param form_edit: Bolean para saber si sera un formulario para editar usuario
        :return: objeto Form de acuerdo a parametros
        """
        department = province = None
        
        
        # Validamos que el listado este en la respuesta
        # si no cumple las validaciones por Default el valor sera None
        # Si el usuario tiene department, traemos provincia
        if specilist and 'address' in specilist and 'department' in specilist['address']:
            department = specilist['address']['department']

        if specilist and 'address' in specilist and 'province' in specilist['address']:
            province = specilist['address']['province']

        return SpecialistForm(data=data, files=files, department=department,
                              province=province, initial=specilist, form_edit=form_edit)

    @method_decorator(login_required)
    def edit(self, request, id):
        ObjApi = api()
        token = request.session['token']
        
        if request.method == 'POST':
            form = self.generateFormSpecialist(data=request.POST, form_edit=True,
                                               files=request.FILES)

            # check whether it's valid:
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

                # return JsonResponse(data)
                result = ObjApi.put(slug='specialists/' + id, token=token, arg=data)

                if result and 'id' in result:
                    if 'photo' in request.FILES:
                        photo = {'photo': request.FILES['photo']}
                        ObjApi.put(slug='upload_photo/' + id, token=token, files=photo)

                    return HttpResponseRedirect(reverse(self._list))
                else:
                    # Mostrar Errores en Form
                    form.add_error_custom(
                        add_errors=result)  # Agregamos errores retornados por la app para este formulario

                    return render(request, 'admin/actor/specialistsForm.html', {'form': form})

        else:
            specilist = ObjApi.get(slug='specialists/' + id, token=token)

            form = self.generateFormSpecialist(specilist=specilist, form_edit=True)

        title_page = _('edit specialist').title()
        vars_page = self.generateHeader(custom_title=title_page)
        specialists_form = reverse(self._edit, args=(id,))
        return render(request, 'admin/actor/specialistsForm.html',
                      {'vars_page': vars_page, 'form': form, 'specialists_form': specialists_form})

    @method_decorator(login_required)
    def delete(self, request):
        if request.method == 'POST':
            id = request.POST['id']
            ObjApi = api()
            result = ObjApi.delete(slug='specialists/' + id, token=request.session['token'])

            return JsonResponse({'result': result})

        return JsonResponse({})


class Client(Actor):
    _list = 'dashboard:actor-clients-list'
    _delete = 'dashboard:actor-clients-delete'
    _detail = 'dashboard:actor-clients-detail'
    _create = 'dashboard:actor-clients-create'
    _edit = 'dashboard:actor-clients-edit'
    vars_page = {
        'btn_clients_class': 'active',
        'name_create_URL': _create,
    }

    @method_decorator(login_required)
    def list(self, request):
        ObjApi = api()
        actual_page = getActualPage(request)
        token = request.session['token']
        filters = {}

        

        # Traer data para el listado
        data = ObjApi.get(slug='clients/', arg=filters, token=token)

        # Definimos columnas adicionales/personalizadas
        custom_column = {
            "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}}
        }
        # Atributos para aplicar a la columna RUC
        attributes_colum = {
            "ruc":
                {
                    "class": "numeric"
                },
            "document_number":
                {
                    "class": "numeric"
                }
        }

        # Coloca los nombres de las cabeceras y a que columna van asociada, customColum tendra prioriedad
        lastnames_title = "{} / {}".format(_("names"), _("business name"))
        header_tabla = [(lastnames_title, "business_name"),( _("alias"), "nick"),( _("code"), "code"),(
                        _("email"), "email_exact"),(_("identification document"), "document_number"),(
                        _("RUC"), "ruc"),( _("querys"), ""),(_("detail"), "detail")]
        tabla = convert(data, header=header_tabla, actual_page=actual_page, custom_column=custom_column,
                        attributes_colum=attributes_colum)

        # Titulo de la vista y variables de la Clase
        title_page = _('clients').title()
        vars_page = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/clientsList.html',
                      {'tabla': tabla, 'vars_page': vars_page})

    @method_decorator(login_required)
    def detail(self, request, id):
        ObjApi = api()
        data = ObjApi.get(slug='clients/' + id, token=request.session['token'])

        # Si la data del usuario no es valida
        if type(data) is not dict or 'id' not in data:
            raise Http404()

        # Titulo de la vista y variables de la Clase
        title_page = "{} - {}".format(_('specialist').title(), _('detail').title())
        vars_page = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/clientsDetail.html', {'data': data, 'vars_page': vars_page})

    @method_decorator(login_required)
    def create(self, request):
        pass

    @method_decorator(login_required)
    def edit(self, request, id):
        pass

    @method_decorator(login_required)
    def delete(self, request):
        pass


class Seller(Actor):
    _list = 'dashboard:actor-sellers-list'
    _delete = 'dashboard:actor-sellers-delete'
    _detail = 'dashboard:actor-sellers-detail'
    _create = 'dashboard:actor-sellers-create'
    _edit = 'dashboard:actor-sellers-edit'
    _list_clients = 'dashboard:actor-clients-list'
    vars_page = {
        'btn_sellers_class': 'active',
        'name_create_URL': _create,
    }

    @method_decorator(login_required)
    def list(self, request):
        ObjApi = api()
        actual_page = getActualPage(request)
        token = request.session['token']
        title_page = _('sellers').title()
        filters = {}

        form_filters = SellerFormFilters(request.GET)
        
        if form_filters.is_valid():
            filters = form_filters.cleaned_data

        
        # Traer data para el listado
        data = ObjApi.get(slug='sellers/', arg=filters, token=token)

        # Definimos columnas adicionales/personalizadas
        custom_column = {
            "last_name": {'type': 'concat', 'data': ('last_name', 'first_name'), 'separator': ' '},
            "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}},
            "advance": {'type': 'concat', 'data': ('count_plans_seller','quota'), 'separator': '/'},
            "ubigeo": {'type': 'concat', 'data': {'address': ('department_name', 'province_name', 'district_name')},
                       'separator': '/'},
            "seeclients": {'type': 'link', 'data': {'url': self._list_clients, 'arguments': {'seller': 'id'},
                                                    'text': _('see clients')}},
        }
        # Atributos para aplicar a la columna RUC
        attributes_colum = {
            "ruc":
                {
                    "class": "numeric"
                }
        }

        # Coloca los nombres de las cabeceras y a que columna van asociada, customColum tendra prioriedad
        lastnames_title = "{} {} {}".format(_("surnames"), _("and"), _("names"))

        header_tabla = [(_("detail"), "detail"),( lastnames_title, "last_name"),( _("code"), "code"),(
                        _("email"), "email_exact"),(
                        _("RUC"), "ruc"),( _('see portfolio'), "seeclients"),( _("ubigeo"), "ubigeo"),( _("quota"), "quota"),(
                        _("advance"), "advance"),(
                        _("number of plans sold"), "count_plans_seller"),( _("number of queries"), "count_queries")]

        tabla = convert(data, header=header_tabla, actual_page=actual_page, custom_column=custom_column,
                        attributes_colum=attributes_colum)

        # Titulo de la vista y variables de la Clase
        vars_page = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/sellersList.html',
                      {'tabla': tabla, 'vars_page': vars_page, 'form_filters': form_filters})


class Administrator(Actor):
    vars_page = {
        'btn_administrators_class': 'active',
        'name_create_URL': 'dashboard:actor-administrators-create',
    }

    @method_decorator(login_required)
    def list(self, request):
        actual_page = getActualPage(request)
        arg = {"page": actual_page}
        ObjApi = api()
        data = ObjApi.get(slug='administrators/', arg=arg, token=request.session['token'])

        custom_column = {
            "last_name": {'type': 'concat', 'data': {'username', 'last_name'}},
            "detail": {'type': 'detail', 'data': {'href': 'dashboard:actor-administrators-detail', 'key': 'id'}}
        }
        lastnames_title = "{} {} {}".format(_("surnames"), _("and"), _("names"))
        header_tabla = {lastnames_title: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc",
                        _("category"): "",
                        _("specialty"): "", _("detail"): "detail"}
        tabla = convert(data, header=header_tabla, actual_page=actual_page, custom_column=custom_column)

        vars_page = self.generateHeader(custom_title=_('administrators').title())
        return render(request, 'admin/actor/administratorsList.html', {'tabla': tabla, 'vars_page': vars_page})
