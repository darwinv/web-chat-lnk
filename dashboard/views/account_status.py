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
        table = data_user = ""
        ObjApi = api()
        token = request.session['token']
        title_page = _('Seller').title()
        

        form_filters = AccountStatusSellerFormFilters(data=request.GET,token=token)        
        if form_filters.is_valid():
            filters = form_filters.cleaned_data
            id = filters['seller']

            if id:
                
                actual_page = None
                tools = Tools()
                filters['from_date'] = tools.date_format_to_db(date=filters['from_date'])
                filters['until_date'] = tools.date_format_to_db(date=filters['until_date'])


                if filters['show_sum_column']:
                    filters['page_size'] = 0
                else:
                    actual_page = getActualPage(request)

                # Traer data para el listado
                data = ObjApi.get(slug='account_status/sellers/' + id, arg=filters, token=token)


                # Columnas personalizadas, tienen mayor prioriedad que los campos que retornan de la api
                custom_column = {
                    "purchase__fee__date": {'type': 'date', 'data': ('purchase__fee__date',)},
                    "fee_accumulated": {'type': 'format_price', 'data': ('fee_accumulated',)},
                    "purchase__fee__fee_amount": {'type': 'format_price', 'data': ('purchase__fee__fee_amount',)},
                    "purchase__total_amount": {'type': 'format_price', 'data': ('purchase__total_amount',)},
                    "fee_accumulated": {'type': 'format_price', 'data': ('fee_accumulated',)},
                    "amount_accumulated": {'type': 'format_price', 'data': ('amount_accumulated',)},
                    "pending_payment": {'type': 'eval', 'data': ('float(r["purchase__total_amount"]) - float(r["fee_accumulated"])',), 
                                        'next':{'type':'format_price'} },
                

                    "count_products_c": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])<=1',), 
                                        'next':{'type':'concat','data':('count_products',)} },
                    "fee_accumulated_c": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])<=1',), 
                                        'next':{'type':'concat','data':('fee_accumulated',)} },
                    "purchase__fee__fee_amount_c": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])<=1',), 
                                        'next':{'type':'concat','data':('purchase__fee__fee_amount',)} },
                    "amount_accumulated_c": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])<=1',), 
                                        'next':{'type':'concat','data':('amount_accumulated',)} },


                    "count_products_q": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])>1',), 
                                        'next':{'type':'concat','data':('count_products',)} },
                    "fee_accumulated_q": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])>1',), 
                                        'next':{'type':'concat','data':('fee_accumulated',)} },
                    "purchase__fee__fee_amount_q": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])>1',), 
                                        'next':{'type':'concat','data':('purchase__fee__fee_amount',)} },
                    "amount_accumulated_q": {'type': 'if_eval', 'data': ('int(r["purchase__fee_number"])>1',), 
                                        'next':{'type':'concat','data':('amount_accumulated',)} },


                    "purchase_fee_amount": {'type': 'concat', 'data': ('purchase__fee__fee_amount',)},
                    "purchase__fee__reference_number": {'type': 'concat', 'data': ('purchase__fee__fee_order_number','/','purchase__fee_number')},

                }

                # Cabecera principal, los titulos de la columna seran sobrepuestos si se pasa el listado de cabecera multiple
                header_table = [(_("date"), "purchase__fee__date"),(_("type"), "is_billable"),(
                _("number"), "purchase__code"),(_("code"), "purchase__client__code" ),(_("nick"), "purchase__client__nick" ),(
                _("nombre"), "purchase__product__name" ),(_("query amount"), "purchase__query_amount" ),(
                _("mounth of duration"), "purchase__product__expiration_number"),(
                _("price"), "purchase__total_amount"),(_("Payments Made"), "purchase_fee_amount"),(
                _("Pending payment"), "pending_payment"),(
                _("advance"),"purchase__fee__reference_number"),(
                

                _(""), "count_products_c"),(_(""), "fee_accumulated_c"),(_(""), "purchase__fee__fee_amount_c"),(_(""), "amount_accumulated_c"),(
                _(""), "count_products_q"),(_(""), "fee_accumulated_q"),(_(""), "purchase__fee__fee_amount_q"),(_(""), "amount_accumulated_q"),(
                _(""), "count_products" ),(_(""), "fee_accumulated" ),(_(""), "purchase__fee__fee_amount"),(_(""),"amount_accumulated")]


                # Multiples header, una lista por cada nivel de la cabecera 
                multi_header = [
                                [
                                    (_('date'), {'rowspan':'4'}),
                                    (_('reference of sale'), {'rowspan': '3','colspan':'2'}),
                                    (_('customer reference'), {'rowspan': '3','colspan':'2'}),
                                    (_('description of plans'), {'rowspan': '3','colspan':'3'}),
                                    (_('sales productivity'), {'rowspan': '3', 'colspan': '4'}),
                                    (_('Composition of the Sale by Form of Payment'), {'rowspan': '1', 'colspan': '12'}),
                                ],
                                [
                                    (_('Cash'), {'colspan': '4'}),
                                    (_('Credit'), {'colspan': '4'}),
                                    (_('Totals'), {'colspan': '4'}),
                                ],                
                                [
                                    (_('units'), {'colspan': '2'}),
                                    (_('amount'), {'colspan': '2'}),
                                    (_('units'), {'colspan': '2'}),
                                    (_('amount'), {'colspan': '2'}),
                                    (_('units'), {'colspan': '2'}),
                                    (_('amount'), {'colspan': '2'}),                                  
                                ],
                                [
                                    (_('type'), {}),
                                    (_('number'), {}),
                                    (_('code '), {}),
                                    (_('Nick'), {}),
                                    (_('name'), {}),
                                    (_('N° of queries'), {}),
                                    (_('mounth of duration'), {}),
                                    (_('Price'), {}),
                                    (_('Payments Made'), {}),
                                    (_('Pending payment'), {}),
                                    (_("reference fee"), {}),                                    
                                    (_('quantity'), {}),
                                    (_('accumulated'), {}),
                                    (_('paid out'), {}),
                                    (_('accumulated'), {}),
                                    (_('quantity'), {}),
                                    (_('accumulated'), {}),
                                    (_('paid out'), {}),
                                    (_('accumulated'), {}),
                                    (_('quantity'), {}),
                                    (_('accumulated'), {}),
                                    (_('paid out'), {}),
                                    (_('accumulated'), {}),
                                ],
                            ]


                if filters['show_sum_column']:
                    # Lista con los valores para el footer de la tabla, posterior al cargado de la data
                    footer = [
                            {
                                'purchase__total_amount':{'type':'acum','id':'purchase__id','value':'purchase__total_amount','format_price':True},
                                'purchase_fee_amount':{'type':'acum','id':'purchase__fee__id','value':'purchase__fee__fee_amount','format_price':True},
                                'pending_payment':{'type':'eval','data':'float(f[0]["_purchase__total_amount"])-float(f[0]["_purchase_fee_amount"])','format_price':True},
                            },
                            {
                                'purchase_fee_amount':{'type':'eval','data':'float(f[0]["_purchase_fee_amount"])/float(f[0]["_purchase__total_amount"])','format_price':True},
                                'pending_payment':{'type':'eval','data':'1-float(f[1]["_purchase_fee_amount"])','format_price':True},
                            }
                          ]
                else:
                    footer = None


                table = convert(data, header=header_table, actual_page=actual_page, custom_column=custom_column,multi_header=multi_header,footer=footer)




                data_user = ObjApi.get(slug='sellers/' + id, token=token)



        vars_page = self.generateHeader(custom_title=title_page)
        return render(request, 'admin/account_status/account_status_seller.html',
                {'vars_page': vars_page, 'table': table, 'form_filters': form_filters, 'data_user': data_user})