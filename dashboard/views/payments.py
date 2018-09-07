from django.shortcuts import render
from dashboard.json2table import convert
from django.utils.translation import ugettext_lazy as _
from dashboard.forms import PendingPaymentFilter, PendingPaymentForm
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
        # actual_page = get_actual_page(request)
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
                header_table = [(_("date"), "created_at"),
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
                    "created_at": {'type': 'datetime', 'data': ('created_at',)},
                    "is_fee": {
                        'type': 'if_eval',
                        'data': ('r["is_fee"]',),
                        'next': {'type': 'concat', 'data': (_("yes").title(),)},
                        'next_elif': {'type': 'concat', 'data': (_("no").title(),)},
                    },
                }
                
                table = convert(data.json(), header=header_table, custom_column=custom_column)

        

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

    # def generate_form(self, data=None, files=None, specialist=None, form_edit=None):
    #     """
    #     Funcion para generar traer formulario de especialistas

    #     :param data: objeto POST o dict de valores relacional
    #     :param specialist: dict que contiene los valores iniciales del usuario
    #     :param form_edit: Bolean para saber si sera un formulario para editar usuario
    #     :return: objeto Form de acuerdo a parametros
    #     """
    #     department = province = None


    #     # Validamos que el listado este en la respuesta
    #     # si no cumple las validaciones por Default el valor sera None
    #     # Si el usuario tiene department, traemos provincia
    #     if specialist and 'address' in specialist and type(specialist['address']) is dict and 'department' in specialist['address']:
    #         department = specialist['address']['department']

    #     if specialist and 'address' in specialist and type(specialist['address']) is dict and 'province' in specialist['address']:
    #         province = specialist['address']['province']

    #     return PendingPaymentForm(data=data, files=files, department=department,
    #                           province=province, initial=specialist, form_edit=form_edit)
