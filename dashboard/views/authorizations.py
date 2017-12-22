"""Vista de Autorizaciones (Clientes/Especialistas/Vendedores)."""
from django.shortcuts import render
from dashboard.json2table import convert
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from api.connection import api
from django.utils.decorators import method_decorator
from dashboard.tools import capitalize as cap, ToolsBackend as Tools
from dashboard.forms import AuthorizationClientFilter
class Autorization:
    logo_content_header = "fa fa-key"
    vars_page = {}
    def generate_header(self, custom_title=None):
        if custom_title:
            title = "{} - ".format(_("authorizations")).title() + custom_title
        else:
            title = self.title_content_header

        header = {'icon': self.logo_content_header, 'title': title}
        return {**header, **self.vars_page}


class AutorizationClient(Autorization):
    """
        Manejo de autorizaciones de clientes,
        se listan los clientes, en orden de pendiente,
        aprobado y rechazado, segun fecha
        Para posterior aprovacion o rechazo
    """

    @method_decorator(login_required)
    def list(self, request):
        """
            Listado de clientes por autorizar,
            se incluyen tambien clientes aprovados y rechazados
        """

        obj_api = api()
        # actual_page = get_actual_page(request)
        token = request.session['token']
        title_page = _('User - User Affiliation').title()
        filters = {}

        form_filters = AuthorizationClientFilter(request.GET)

        if form_filters.is_valid():  # Agregamos filtros de encontrarse alguno
            filters = form_filters.cleaned_data
            tools = Tools()
            filters['from_date'] = tools.date_format_to_db(date=filters['from_date'])
            filters['until_date'] = tools.date_format_to_db(date=filters['until_date'])
            filters = form_filters.cleaned_data
        
        if request.method == 'GET':
            if 'approve' in request.GET and request.GET['approve']:
                pk = request.GET['approve']
                data = {"status":1}
                obj_api.put(slug='authorizations/clients/' + pk, token=token, arg=data)

            if 'rejected' in request.GET and request.GET['rejected']:
                pk = request.GET['rejected']
                data = {"status":2}
                obj_api.put(slug='authorizations/clients/' + pk, token=token, arg=data)

        # Traer data para el listado
        data = obj_api.get(slug='authorizations/clients/', arg=filters, token=token)


        header_table = [("", "code_seller"), ("", "name"),(
                        "", "document_type_name"), ( "", "document"),(
                        "", ""), ("", ""), (
                        "", "document"), (
                        "", "approve"), ("", "rejected"), (
                        "", "date_join")]

        # Multiples header, una lista por cada nivel de la cabecera
        multi_header = [
            [
                (_("seller code"), {'rowspan': '2'}),
                (_('user'), {'rowspan': '1', 'colspan': '3'}),
                (_('product'), {'rowspan': '1', 'colspan': '2'}),
                (_('user code'), {'rowspan': '2', 'colspan': '1'}),
                (_('validation'), {'rowspan': '1', 'colspan': '2'}),
                (_('date'), {'rowspan': '2', 'colspan': '1'}),
            ],
            [
                (_('name or Social reason'), {}),
                (_('type document'), {}),
                (_('document number'), {}),
                (_('description'), {}),
                (_('Query Numbers'), {}),
                (_('approve'), {}),
                (_('deneis'), {}),
            ],
        ]

        approve_column = {'type': 'submit', 'data': {'name':'approve','key':'id',
                                                    'cls':'btn btn-success','text':cap(_('approve'))}}
        rejected_column = {'type': 'submit', 'data': {'name':'rejected','key':'id',
                                                    'cls':'btn btn-danger','text':cap(_('rejected'))}}
        custom_column = {
            "date_join": {'type': 'date', 'data': ('date_join',)},
            "approve": {'type': 'if_eval', 'data': ('r["status"]=="0"',),
                                         'next': approve_column},
            "rejected": {'type': 'if_eval', 'data': ('r["status"]=="0"',),
                                         'next': rejected_column},
        }

        table = convert(data, header=header_table, multi_header=multi_header, custom_column=custom_column)

        # Titulo de la vista y variables de la Clase
        vars_page = self.generate_header(custom_title=title_page)

        return render(request, 'admin/authorization/clients.html',
                      {'table': table, 'vars_page': vars_page, 'form_filters':form_filters})