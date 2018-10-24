from django.shortcuts import render
from dashboard.json2table import convert, get_actual_page
from django.utils.translation import ugettext_lazy as _
from dashboard.forms import PendingPaymentFilter, PendingPaymentForm
from dashboard.forms import PaymentMatch
from login.utils.tools import role_admin_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from api.connection import api
from django.http import HttpResponseRedirect
from django.urls import reverse

class Payment:
    logo_content_header = "fa fa-credit-card"
    vars_page = {}
    def generate_header(self, custom_title=None):
        if custom_title:
            title = "{} - ".format(_("payments")).title() + custom_title
        else:
            title = self.title_content_header

        header = {'icon': self.logo_content_header, 'title': title}
        return {**header, **self.vars_page}


class PaymentsPending(Payment):
    """
        Manejo de autorizaciones de clientes,
        se listan los clientes, en orden de pendiente,
        aprobado y rechazado, segun fecha
        Para posterior aprovacion o rechazo
    """
    # _detail = 'dashboard:payment-fee-form'
    _detail = 'dashboard:payments-pending-detail'
    _list = 'dashboard:payments-pending'

    @method_decorator(user_passes_test(role_admin_check()))
    def list(self, request):
        """
            Listado de clientes por autorizar,
            se incluyen tambien clientes aprovados y rechazados
        """

        obj_api = api()
        actual_page = get_actual_page(request)

        token = request.session['token']
        title_page = _('payments').title()+" - "+ _('pending').title()
        filters = {}
        table = ""

        form_filters = PendingPaymentFilter(request.GET)
        if form_filters.is_valid():  # Agregamos filtros de encontrarse alguno
            filters = form_filters.cleaned_data

            # Traer data para el listado
            data = obj_api.get_all(slug='sales/payment-pending/', arg=filters, token=token)
            
            if data.status_code == 400:
                form_filters.add_error_custom(add_errors=data.json())
            else:
                lastnames_title = "{} / {}".format(_("names"), _("business name"))
                header_table = [(_("date"), "pay_before"),
                                (lastnames_title, "business_name"),
                                ("total", "total_amount"),
                                (_("fee").title(), "is_fee"),(_("detail"), "detail")]


                # Definimos columnas adicionales/personalizadas
                custom_column = {
                    "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}},
                    "business_name": {
                        'type': 'if_eval',
                        'data': ('r["client__business_name"]',),
                        'next': {'type': 'concat', 'data': ('client__business_name',)},
                        'next_elif': {'type': 'concat', 'data': ('client__last_name', ' ', 'client__first_name')},
                    },
                    "pay_before": {'type': 'date', 'data': ('pay_before',)},
                    "is_fee": {
                        'type': 'if_eval',
                        'data': ('r["is_fee"]',),
                        'next': {'type': 'concat', 'data': (_("yes").title(),)},
                        'next_elif': {'type': 'concat', 'data': (_("no").title(),)},
                    },
                }
                
                table = convert(data.json(), header=header_table, custom_column=custom_column,
                                actual_page=actual_page)

        

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/payment/pending.html',
                      {'vars_page': vars_page, 'form_filters':form_filters, 'table':table})


    @method_decorator(user_passes_test(role_admin_check()))
    def detail(self, request, pk):
        obj_api = api()
        token = request.session['token']

        data = obj_api.get_all(slug='fees/payment-pending/' + pk, token=token)

        if data.status_code == 200:
            # Titulo de la vista y variables de la Clase
            title_page = _('payments').title()+" - "+ _('pending').title()
            vars_page = self.generate_header(custom_title=title_page)
            
            data_json = data.json()
            if request.method == 'POST':

                form = PendingPaymentForm(data=request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    result = obj_api.post_all(slug='payment/', token=token, arg=data)
                    
                    if result and result.status_code == 201:
                        return HttpResponseRedirect(reverse(self._list))
                    else:
                        # Mostrar Errores en Form
                        # Agregamos errores retornados por la app para este formulario
                        form.add_error_custom(
                                add_errors=result.json())
            else:
                payment = {}
                payment['bank'] = 1
                payment['monthly_fee'] = data_json['id']
                form = PendingPaymentForm(initial=payment)

            return render(request, 'admin/payment/pending_detail.html', 
                {'data': data_json, 'vars_page': vars_page,
                 'form': form})
        else:
            return HttpResponseRedirect(reverse(self._list))


class PaymentsClientMatch(Payment):
    """
        Manejo de autorizaciones de clientes,
        se listan los clientes, en orden de pendiente,
        aprobado y rechazado, segun fecha
        Para posterior aprovacion o rechazo
    """
    # _detail = 'dashboard:payment-fee-form'
    _detail = 'dashboard:payments-client-match-detail'
    _list = 'dashboard:payments-client-match'

    @method_decorator(user_passes_test(role_admin_check()))
    def list(self, request):
        """
            Listado de clientes por autorizar,
            se incluyen tambien clientes aprovados y rechazados
        """

        obj_api = api()
        actual_page = get_actual_page(request)

        token = request.session['token']
        title_page = _('payments').title()+" - "+ _('match specialist').title()
        filters = {}
        table = ""

        form_filters = PendingPaymentFilter(request.GET)
        if form_filters.is_valid():  # Agregamos filtros de encontrarse alguno
            filters = form_filters.cleaned_data
            filters["status"] = 4
            
            # Traer data para el listado
            data = obj_api.get_all(slug='backend/matchs/', arg=filters, token=token)
            
            if data.status_code == 400:
                form_filters.add_error_custom(add_errors=data.json())
            else:
                
                header_table = [(_("date"), "date"),
                                (_("client"), "client"),
                                (_("specialist"), "specialist"),                                
                                (_("category"), "category"),
                                (_("detail"), "detail"),]


                # Definimos columnas adicionales/personalizadas
                custom_column = {
                    "date": {'type': 'datetime', 'data': ('date',)},                    
                    "client": {
                        'type': 'if_eval',
                        'data': ('r["client"]["business_name"]',),
                        'next': {'type': 'concat', 'data': {'client': ('business_name',)}},
                        'next_elif': {'type': 'concat', 'data': {'client': ('last_name',' ','first_name')}},
                    },
                    "specialist": {
                        'type': 'concat', 
                        'data': {'specialist': ('last_name',' ','first_name')},
                    },
                    "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}}                    
                }
                
                table = convert(data.json(), header=header_table, custom_column=custom_column,
                                actual_page=actual_page)

        

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/payment/pending.html',
                      {'vars_page': vars_page, 'form_filters':form_filters, 'table':table
                       })

    @method_decorator(user_passes_test(role_admin_check()))
    def detail(self, request, pk):
        obj_api = api()
        token = request.session['token']

        data = obj_api.get_all(slug='backend/matchs/' + pk, token=token)

        if data.status_code == 200:
            # Titulo de la vista y variables de la Clase
            title_page = _('payments').title()+" - "+ _('pending').title()
            vars_page = self.generate_header(custom_title=title_page)
            
            data_json = data.json()
            if request.method == 'POST':

                form = PaymentMatch(data=request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    result = obj_api.post_all(slug='clients/payment/match/', token=token, arg=data)
                    
                    if result and result.status_code == 201:
                        return HttpResponseRedirect(reverse(self._list))
                    else:
                        # Mostrar Errores en Form
                        # Agregamos errores retornados por la app para este formulario
                        form.add_error_custom(
                                add_errors=result.json())
            else:
                payment = {}
                payment['bank'] = 1
                payment['match'] = data_json['id']
                form = PaymentMatch(initial=payment)

            return render(request, 'admin/payment/match.html',  
                {'data': data_json, 'vars_page': vars_page,
                 'form': form, 'go_back':self._list})
        else:
            return HttpResponseRedirect(reverse(self._list))

class PaymentsSpecialistMatch(Payment):
    """
        Manejo de autorizaciones de clientes,
        se listan los clientes, en orden de pendiente,
        aprobado y rechazado, segun fecha
        Para posterior aprovacion o rechazo
    """
    # _detail = 'dashboard:payment-fee-form'
    _detail = 'dashboard:payments-specialist-match-detail'
    _list = 'dashboard:payments-specialist-match'

    @method_decorator(user_passes_test(role_admin_check()))
    def list(self, request):
        """
            Listado de clientes por autorizar,
            se incluyen tambien clientes aprovados y rechazados
        """

        obj_api = api()
        actual_page = get_actual_page(request)

        token = request.session['token']
        title_page = _('payments').title()+" - "+ _('match specialist').title()
        filters = {}
        table = ""

        form_filters = PendingPaymentFilter(request.GET)
        if form_filters.is_valid():  # Agregamos filtros de encontrarse alguno
            filters = form_filters.cleaned_data
            filters["status"] = 2
            filters["payment_option_specialist"] = 1
            
            # Traer data para el listado
            data = obj_api.get_all(slug='backend/matchs/', arg=filters, token=token)
            
            if data.status_code == 400:
                form_filters.add_error_custom(add_errors=data.json())
            else:
                
                header_table = [(_("date"), "date"),
                                (_("client"), "client"),
                                (_("specialist"), "specialist"),                                
                                (_("category"), "category"),
                                (_("detail"), "detail"),]

                # Definimos columnas adicionales/personalizadas
                custom_column = {
                    "date": {'type': 'datetime', 'data': ('date',)},                    
                    "client": {
                        'type': 'if_eval',
                        'data': ('r["client"]["business_name"]',),
                        'next': {'type': 'concat', 'data': {'client': ('business_name',)}},
                        'next_elif': {'type': 'concat', 'data': {'client': ('last_name',' ','first_name')}},
                    },
                    "specialist": {
                        'type': 'concat', 
                        'data': {'specialist': ('last_name',' ','first_name')},
                    },
                    "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}}                    
                }

                table = convert(data.json(), header=header_table, custom_column=custom_column,
                                actual_page=actual_page)

        

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/payment/pending.html',
                      {'vars_page': vars_page, 'form_filters':form_filters, 'table':table})


    @method_decorator(user_passes_test(role_admin_check()))
    def detail(self, request, pk):
        obj_api = api()
        token = request.session['token']
        
        data = obj_api.get_all(slug='backend/matchs/' + pk, token=token)
        
        if data.status_code == 200:
            # Titulo de la vista y variables de la Clase
            title_page = _('payments').title()+" - "+ _('pending').title()
            vars_page = self.generate_header(custom_title=title_page)
            
            data_json = data.json()
            if request.method == 'POST':
                form = PaymentMatch(data=request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    result = obj_api.post_all(slug='specialists/payment/match/', token=token, arg=data)
                    
                    if result and result.status_code == 201:
                        return HttpResponseRedirect(reverse(self._list))
                    else:
                        # Mostrar Errores en Form
                        # Agregamos errores retornados por la app para este formulario
                        form.add_error_custom(
                                add_errors=result.json())
            else:
                payment = {}
                payment['bank'] = 1
                payment['match'] = data_json['id']
                form = PaymentMatch(initial=payment)
            
            return render(request, 'admin/payment/match.html', 
                {'data': data_json, 'vars_page': vars_page,
                 'form': form, 'go_back':self._list})
        else:
            return HttpResponseRedirect(reverse(self._list))


class AuthorizationSpecialistMatch(Payment):
    """
        Manejo de autorizaciones de clientes,
        se listan los clientes, en orden de pendiente,
        aprobado y rechazado, segun fecha
        Para posterior aprovacion o rechazo
    """
    # _detail = 'dashboard:payment-fee-form'
    _detail = 'dashboard:authorization-specialist-match-detail'
    _list = 'dashboard:authorization-specialist-match'

    @method_decorator(user_passes_test(role_admin_check()))
    def list(self, request):
        """
            Listado de clientes por autorizar,
            se incluyen tambien clientes aprovados y rechazados
        """

        obj_api = api()
        actual_page = get_actual_page(request)

        token = request.session['token']
        title_page = _('payments').title()+" - "+ _('match specialist').title()
        filters = {}
        table = ""

        form_filters = PendingPaymentFilter(request.GET)
        if form_filters.is_valid():  # Agregamos filtros de encontrarse alguno
            filters = form_filters.cleaned_data
            filters["status"] = 2
            filters["payment_option_specialist"] = 2
            
            # Traer data para el listado
            data = obj_api.get_all(slug='backend/matchs/', arg=filters, token=token)
            
            if data.status_code == 400:
                form_filters.add_error_custom(add_errors=data.json())
            else:
                
                header_table = [(_("date"), "date"),
                                (_("client"), "client"),
                                (_("specialist"), "specialist"),                                
                                (_("category"), "category"),
                                (_("detail"), "detail"),]


                # Definimos columnas adicionales/personalizadas
                custom_column = {
                    "date": {'type': 'datetime', 'data': ('date',)},                    
                    "client": {
                        'type': 'if_eval',
                        'data': ('r["client"]["business_name"]',),
                        'next': {'type': 'concat', 'data': {'client': ('business_name',)}},
                        'next_elif': {'type': 'concat', 'data': {'client': ('last_name',' ','first_name')}},
                    },
                    "specialist": {
                        'type': 'concat', 
                        'data': {'specialist': ('last_name',' ','first_name')},
                    },
                    "detail": {'type': 'detail', 'data': {'url': self._detail, 'key': 'id'}}                    
                }
                
                table = convert(data.json(), header=header_table, custom_column=custom_column,
                                actual_page=actual_page)

        

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/payment/pending.html',
                      {'vars_page': vars_page, 'form_filters':form_filters, 'table':table})

    @method_decorator(user_passes_test(role_admin_check()))
    def detail(self, request, pk):
        obj_api = api()
        token = request.session['token']

        data = obj_api.get_all(slug='backend/matchs/' + pk, token=token)

        if data.status_code == 200:
            # Titulo de la vista y variables de la Clase
            title_page = _('payments').title()+" - "+ _('pending').title()
            vars_page = self.generate_header(custom_title=title_page)
            
            data_json = data.json()
            if request.method == 'POST':
                result = obj_api.put_all(slug='confirm-discount/{}'.format(pk), token=token)

                if result and result.status_code == 200:
                    return HttpResponseRedirect(reverse(self._list))
            

            return render(request, 'admin/authorization/specialist_match.html', 
                {'data': data_json, 'vars_page': vars_page})
        else:
            return HttpResponseRedirect(reverse(self._list))

