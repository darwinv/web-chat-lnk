from django.shortcuts import render
from dashboard.json2table import convert
from django.utils.translation import ugettext_lazy as _
from dashboard.forms import PendingPaymentFilter
from login.utils.tools import role_admin_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from api.connection import api

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
    _detail = 'dashboard:actor-clients-detail'

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
