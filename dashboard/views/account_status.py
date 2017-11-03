from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from api.connection import api
from dashboard.json2table import convert, getActualPage
from dashboard.tools import ToolsBackend as Tools
from dashboard.forms import AccountStatusSellerFormFilters
from django.shortcuts import render
import pdb



class AccountStatus:
    vars_page = {}
    logo_content_header = "fa fa-calculator"

    def generateHeader(self, custom_title=None):
        if custom_title:
            title = "{} - ".format(_("Account Status")).title() + custom_title
        else:
            title = self.title_content_header

        header = {'icon': self.logo_content_header, 'title': title}
        return {**header, **self.vars_page}

class AccountStatusSeller(AccountStatus):

    @method_decorator(login_required)
    def list(self, request):
        """
            Listado de estado de cuenta de vendedores, donde se debera filtrar para buscar
            las ventas de un vendedor en especifico.
        """
        table = ""
        ObjApi = api()
        token = request.session['token']
        title_page = _('Seller').title()
        

        form_filters = AccountStatusSellerFormFilters(data=request.GET,token=token)        
        if form_filters.is_valid():
            filters = form_filters.cleaned_data
            id = filters['seller']

            if id:
                actual_page = getActualPage(request)
                
                tools = Tools()
                filters['from_date'] = tools.set_date_format(date=filters['from_date'])
                filters['until_date'] = tools.set_date_format(date=filters['until_date'])
                
                # Traer data para el listado
                data = ObjApi.get(slug='account_status/sellers/' + id, arg=filters, token=token)

                header_table = [(_("date"), "purchase__fee__date"),(_("type"), "purchase__product__is_billable"),(_("number"), "purchase__code"),(
                _("code"), "purchase__client__code" ),(
                _("nick"), "purchase__client__nick" ),(_("nombre"), "purchase__product__name" ),(_("N° queries"), "purchase__query_amount" ),(
                _("query amount"), "purchase__query_amount" ),(
                _("duration"), "purchase__product__expiration_number"),(_("price"), "purchase__fee__fee_amount"),(_("price"), "purchase__total_amount"),(
                _("payment made"), "purchase__fee__fee_amount"),(_("price"), "purchase__fee__fee_amount"),(_("accumulated"), "fee_accumulated"),(
                _("accumulated"), "fee_accumulated"),( _("accumulated"), "fee_accumulated" ),( _("paid out"), "purchase__fee__fee_amount" ),(
                _("accumulated"), "amount_accumulated")]

                table = convert(data, header=header_table, actual_page=actual_page)


        vars_page = self.generateHeader(custom_title=title_page)
        return render(request, 'admin/account_status/account_status_seller.html',
                {'vars_page': vars_page, 'table': table, 'form_filters': form_filters})