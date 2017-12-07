"""Vista de Actores (Clientes/Especialistas/Vendedores)."""
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from api.connection import api

from dashboard.json2table import convert, get_actual_page
from dashboard.forms import SpecialistForm, SellerForm, SellerFormFilters


class Actor:
    logo_content_header = "fa fa-users"

    def generate_header(self, custom_title=None):
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
        obj_api = api()
        filters = {}
        actual_page = get_actual_page(request)
        arg = {"page": actual_page}
        token = request.session['token']
        title_page = _('specialists').title()

        # Filtro de especialista principal
        if 'main_specialist' in request.GET:
            main_specialist = request.GET['main_specialist']
            arg.update({"main_specialist": main_specialist})
            data_main_specilist = obj_api.get(slug='specialists/' + main_specialist, token=token)
            filters.update({'main_specialist': data_main_specilist})
            title_page = _('associated specialists').title()

        # Traer data para el listado
        data = obj_api.get(slug='specialists/', arg=arg, token=token)

        # Definimos columnas adicionales/personalizadas
        custom_column = {
            "last_name": {'type': 'concat', 'data': ('last_name', ' ', 'first_name')},
            "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}},
            "delete": {'type': 'delete', 'data': {'url': self._delete, 'key': 'id'}}
        }
        # Atributos para aplicar a la columna RUC
        attributes_column = {
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
                        attributes_column=attributes_column)

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/actor/specialistsList.html',
                      {'tabla': tabla, 'vars_page': vars_page, 'filters': filters})

    @method_decorator(login_required)
    def detail(self, request, pk):
        obj_api = api()
        token = request.session['token']

        data = obj_api.get(slug='specialists/' + pk, token=token)

        # Si la data del usuario no es valida
        if not data and type(data) is not dict:
            raise Http404()

        # Si esta definido el tipo de especialista que es el usuario
        if type(data) is dict and 'type_specialist' in data:
            type_specialist = data['type_specialist']
        else:
            type_specialist = ''


        # Titulo de la vista y variables de la Clase
        title_page = "{} {} - {}".format(_('specialist').title(), _(type_specialist), _('detail').title())
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/actor/specialistsDetail.html', {'data': data, 'vars_page': vars_page})

    @method_decorator(login_required)
    def create(self, request):
        obj_api = api()
        token = request.session['token']

        # Si llega envio por POST se valida contra el SpecialistForm
        if request.method == 'POST':
            form = self.generate_form_specialist(data=request.POST, files=request.FILES)
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

                result = obj_api.post(slug='specialists/', token=token, arg=data)

                if result and 'id' in result:

                    if 'photo' in request.FILES:
                        photo = {'photo': request.FILES['photo']}
                        obj_api.put(slug='upload_photo/' + str(result['id']), token=token, files=photo)
                    # Process success

                    if 'img_document_number' in request.FILES:
                        img_document_number = {'img_document_number': request.FILES['img_document_number']}
                        obj_api.put(slug='upload_document/' + str(result['id']), token=token, files=img_document_number)
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
            form = self.generate_form_specialist()

        title_page = _('create specialist').title()
        vars_page = self.generate_header(custom_title=title_page)
        specialists_form = reverse(self._create)
        return render(request, 'admin/actor/specialistsForm.html',
                      {'vars_page': vars_page, 'form': form, 'specialists_form': specialists_form})

    @method_decorator(login_required)
    def edit(self, request, pk):
        obj_api = api()
        token = request.session['token']

        if request.method == 'POST':
            form = self.generate_form_specialist(data=request.POST, form_edit=True,
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
                result = obj_api.put(slug='specialists/' + pk, token=token, arg=data)

                if result:
                    # Agregando foto del Usuario
                    if 'photo' in request.FILES:
                        photo = {'photo': request.FILES['photo']}
                        obj_api.put(slug='upload_photo/' + pk, token=token, files=photo)

                    # Se agrega documento del usuario
                    if 'img_document_number' in request.FILES:
                        img_document_number = {'img_document_number': request.FILES['img_document_number']}
                        obj_api.put(slug='upload_document/' + pk, token=token, files=img_document_number)


                    return HttpResponseRedirect(reverse(self._list))
                else:
                    # Mostrar Errores en Form
                    form.add_error_custom(
                        add_errors=result)  # Agregamos errores retornados por la app para este formulario

                    return render(request, 'admin/actor/specialistsForm.html', {'form': form})
            else:
                print(form.errors)
                print("------------------------------------")
        else:
            specilist = obj_api.get(slug='specialists/' + pk, token=token)

            form = self.generate_form_specialist(specilist=specilist, form_edit=True)

        title_page = _('edit specialist').title()
        vars_page = self.generate_header(custom_title=title_page)
        specialists_form = reverse(self._edit, args=(pk,))
        return render(request, 'admin/actor/specialistsForm.html',
                      {'vars_page': vars_page, 'form': form, 'specialists_form': specialists_form})


    def generate_form_specialist(self, data=None, files=None, specilist=None, form_edit=None):
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
        if specilist and 'address' in specilist and type(specilist['address']) is dict and 'department' in specilist['address']:
            department = specilist['address']['department']

        if specilist and 'address' in specilist and type(specilist['address']) is dict and 'province' in specilist['address']:
            province = specilist['address']['province']

        return SpecialistForm(data=data, files=files, department=department,
                              province=province, initial=specilist, form_edit=form_edit)


    @method_decorator(login_required)
    def delete(self, request):
        if request.method == 'POST':
            id = request.POST['id']
            obj_api = api()
            result = obj_api.delete(slug='specialists/' + id, token=request.session['token'])

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
        obj_api = api()
        actual_page = get_actual_page(request)
        token = request.session['token']
        filters = {}



        # Traer data para el listado
        data = obj_api.get(slug='clients/', arg=filters, token=token)

        # Definimos columnas adicionales/personalizadas
        custom_column = {
            "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}}
        }
        # Atributos para aplicar a la columna RUC
        attributes_column = {
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
                        attributes_column=attributes_column)

        # Titulo de la vista y variables de la Clase
        title_page = _('clients').title()
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/actor/clientsList.html',
                      {'tabla': tabla, 'vars_page': vars_page})

    @method_decorator(login_required)
    def detail(self, request, id):
        obj_api = api()
        data = obj_api.get(slug='clients/' + id, token=request.session['token'])

        # Si la data del usuario no es valida
        if type(data) is not dict or 'id' not in data:
            raise Http404()

        # Titulo de la vista y variables de la Clase
        title_page = "{} - {}".format(_('specialist').title(), _('detail').title())
        vars_page = self.generate_header(custom_title=title_page)

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
        obj_api = api()
        actual_page = get_actual_page(request)
        token = request.session['token']
        title_page = _('sellers').title()
        filters = {}

        form_filters = SellerFormFilters(request.GET)

        if form_filters.is_valid():
            filters = form_filters.cleaned_data


        # Traer data para el listado
        data = obj_api.get(slug='sellers/', arg=filters, token=token)

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
        attributes_column = {
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
                        attributes_column=attributes_column)

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/actor/sellersList.html',
                      {'tabla': tabla, 'vars_page': vars_page, 'form_filters': form_filters})

    @method_decorator(login_required)
    def create(self, request):
        """Metodo para crear Vendedores."""
        obj_api = api()
        token = request.session["token"]
        # Si llega envio por POST se valida contra el SpecialistForm
        if request.method == 'POST':

            form = self.generate_form_seller(data=request.POST, files=request.FILES)
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
                if 'residence_country' in data:
                    data["residence_country"] = data["residence_country"].id
                nationality = data.get("nationality")
                data["nationality"] = nationality.id

                result = obj_api.post(slug='sellers/', token=token, arg=data)
                if result and 'id' in result:
                    if 'photo' in request.FILES:
                        photo = {'photo': request.FILES['photo']}
                        obj_api.put(slug='upload_photo/' + str(result['id']), token=token, files=photo)
                    # Process success
                    if 'img_document_number' in request.FILES:
                        img_document_number = {'img_document_number': request.FILES['img_document_number']}
                        obj_api.put(slug='upload_document/' + str(result['id']), token=token, files=img_document_number)
                    # Process success
                    return HttpResponseRedirect(reverse(self._list))
                else:
                    # Mostrar Errores en Form
                    form.add_error_custom(
                        add_errors=result)  # Agregamos errores retornados por la app para este formulario

                    return render(request, 'admin/actor/sellersForm.html', {'form': form})

        else:
            # Crear formulario de especialistas vacio, se traeran
            # datos de selecion como Categorias y Departamentos.
            form = self.generate_form_seller()

        # import pdb; pdb.set_trace(
        title_page = _('create seller').title()
        vars_page = self.generate_header(custom_title=title_page)
        sellers_form = reverse(self._create)
        return render(request, 'admin/actor/sellersForm.html',
                      {'vars_page': vars_page, 'form': form, 'sellers_form': sellers_form})

    def generate_form_seller(self, data=None, files=None, seller=None, form_edit=None):
        """
        Funcion para generar traer formulario de especialistas.

        :param data: objeto POST o dict de valores relacional
        :param specilist: dict que contiene los valores iniciales del usuario
        :param form_edit: Bolean para saber si sera un formulario para editar usuario
        :return: objeto Form de acuerdo a parametros.
        """
        department = province = None
        #
        #
        # Validamos que el listado este en la respuesta
        # # si no cumple las validaciones por Default el valor sera None
        # # Si el usuario tiene department, traemos provincia
        # if specilist and 'address' in specilist and 'department' in specilist['address']:
        #     department = specilist['address']['department']
        #
        # if specilist and 'address' in specilist and 'province' in specilist['address']:
        #     province = specilist['address']['province']

        return SellerForm(data=data, files=files, department=department,
                          province=province, initial=seller, form_edit=form_edit)

class Administrator(Actor):
    vars_page = {
        'btn_administrators_class': 'active',
        'name_create_URL': 'dashboard:actor-administrators-create',
    }

    @method_decorator(login_required)
    def list(self, request):
        actual_page = get_actual_page(request)
        arg = {"page": actual_page}
        obj_api = api()
        data = obj_api.get(slug='administrators/', arg=arg, token=request.session['token'])

        custom_column = {
            "last_name": {'type': 'concat', 'data': {'username', 'last_name'}},
            "detail": {'type': 'detail', 'data': {'href': 'dashboard:actor-administrators-detail', 'key': 'id'}}
        }
        lastnames_title = "{} {} {}".format(_("surnames"), _("and"), _("names"))
        header_tabla = {lastnames_title: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc",
                        _("category"): "",
                        _("specialty"): "", _("detail"): "detail"}
        tabla = convert(data, header=header_tabla, actual_page=actual_page, custom_column=custom_column)

        vars_page = self.generate_header(custom_title=_('administrators').title())
        return render(request, 'admin/actor/administratorsList.html', {'tabla': tabla, 'vars_page': vars_page})
