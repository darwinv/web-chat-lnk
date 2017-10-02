from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


from api.connection import api

from dashboard.json2table import convert,getActualPage


#forms
from dashboard.forms import SpecialistForm

class Actor:
    logo_content_header    = "fa fa-users"
    title_content_header   = "{} - ".format(_("actors").title())

    def generateHeader(self,CustomTitle=None):
        if CustomTitle:
            title = self.title_content_header + CustomTitle
        else:
            title = self.title_content_header

        header = {'icon':self.logo_content_header,'title':title}
        return {**header, **self.varsPage}


        
##SPECIALIST##
class Specialist(Actor):
    varsPage = {
                'btnSpecialistsClass':'active',
                'nameCreateURL':'dashboard:actor-specialists-create',
                }

    @method_decorator(login_required)
    def showList(self,request):
        actualPage      = getActualPage(request)
        arg             = {"page": actualPage}
        ObjApi          = api()
        data            = ObjApi.get(slug='specialists/',arg=arg,request=request)

        customColumn    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-specialists-detail','key':'id'}},
                            "delete": {'type':'delete','data':{'class':'deleteSpecialist','key':'id'}}
                          }
        lastnamesTitle  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        header_tabla    = {lastnamesTitle: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("specialty"): "",_("detail"): "detail",_("delete"): "delete"}
        tabla           = convert(data, header=header_tabla,actualPage=actualPage, customColumn=customColumn )

        varsPage        = self.generateHeader(CustomTitle=_('specialists').title())
        return render(request, 'admin/actor/specialistsList.html', {'tabla': tabla,'varsPage':varsPage})


    @method_decorator(login_required)
    def detail(self,request,specialist_id):
        ObjApi = api()
        data   = ObjApi.get(slug='specialists/'+specialist_id,request=request)
        
        CustomTitle     = "{} {} - {}".format(_('specialist').title(),_(data['type_specialist']),_('detail').title())
        varsPage        = self.generateHeader(CustomTitle=CustomTitle)
        
        return render(request, 'admin/actor/specialistsDetail.html',{'data': data,'varsPage':varsPage})


    @method_decorator(login_required)
    def create(self,request):
        ObjApi      = api()

        if request.method == 'POST':
            form = SpecialistForm(data=request.POST)
            # check whether it's valid:
            if form.is_valid():
                result = ObjApi.post(slug='specilist/',request=request)
                return HttpResponseRedirect(reverse('dashboard:actor-specialists-list'))

        else:
            categories  = ObjApi.get(slug='categories/',request=request)
            departments = ObjApi.get(slug='departments/',request=request)
            form        = SpecialistForm(categories=categories['list'],departments=departments['list'])
                
        varsPage    = self.generateHeader(CustomTitle=_('create specialist').title())
        return render(request, 'admin/actor/specialistsForm.html', {'varsPage':varsPage,'form':form})



    @method_decorator(login_required)
    def edit(self,request,specialist_id):
        ObjApi      = api()

        if request.method == 'POST':
            form = SpecialistForm(data=request.POST)
            # check whether it's valid:
            if form.is_valid():
                result = ObjApi.put(slug='specilist/'+specialist_id,request=request)
                return HttpResponseRedirect(reverse('dashboard:actor-specialists-list'))

        else:
            specilist   = ObjApi.get(slug='specialists/'+specialist_id,request=request)
            categories  = ObjApi.get(slug='categories/',request=request)
            departments = ObjApi.get(slug='departments/',request=request)

            if 'department' in specilist:
                arg = {'department':specilist['department']}
                provinces   = ObjApi.get(slug='provinces/',request=request,arg=arg)
            else:
                provinces   = {'list':None}

            if 'district' in specilist:
                arg = {'province':specilist['province']}
                districts   = ObjApi.get(slug='districts/',request=request,arg=arg)
            else:
                districts   = {'list':None}

            form        = SpecialistForm(categories=categories['list'],departments=departments['list'],provinces=provinces['list'],districts=districts['list'],initial=specilist)
        
        varsPage    = self.generateHeader(CustomTitle=_('edit specialist').title())
        return render(request, 'admin/actor/specialistsForm.html', {'varsPage':varsPage,'form':form})

    
    @method_decorator(login_required)
    def delete(self,request):
        if request.method == 'POST':
            specialist_id   = request.POST['specialist_id']
            ObjApi          = api()
            result          = ObjApi.delete(slug='specialists/'+specialist_id,request=request)

            return JsonResponse({'result': result})

        return JsonResponse({})


##CLIENT##
class Client(Actor):    
    varsPage = {
                'btnClientsClass':'active',
                'nameCreateURL':'dashboard:actor-clients-create',
                }

    @method_decorator(login_required)
    def showList(self,request):
        actualPage      = getActualPage(request)
        arg             = {"page": actualPage}
        ObjApi          = api()
        data            = ObjApi.get(slug='clients/',arg=arg,request=request)
        

        customColumn    = {
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-clients-detail','key':'id'}}
                          }
        lastnamesTitle  = "{}/{}".format(_("names"),_("business name"))
        header_tabla    = {lastnamesTitle: "bussiness_name", _("alias"): "nick", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("identification document"): "document_number",_("RUC"): "ruc",_("category"): "",_("consultas"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actualPage=actualPage, customColumn=customColumn )


        varsPage        = self.generateHeader(CustomTitle=_('clients').title())
        return render(request, 'admin/actor/clientsList.html', {'tabla': tabla,'varsPage':varsPage})


##SELLER##
class Seller(Actor):
    varsPage = {
                'btnSellersClass':'active',
                'nameCreateURL':'dashboard:actor-sellers-create',
                }

    @method_decorator(login_required)
    def showList(self,request):
        actualPage      = getActualPage(request)
        arg             = {"page": actualPage}
        ObjApi          = api()
        data            = ObjApi.get(slug='sellers/',arg=arg,request=request)

        customColumn    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-sellers-detail','key':'id'}}
                          }
        lastnamesTitle  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        viewCient       = "{} {}".format(_("view"),_("clients"))
        header_tabla    = {lastnamesTitle: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc",_("viewCient"): "", _("ubigeo"): "",
                           _("fee"): "",_("advance"): "",_("number of plans sold"): "",_("number of queries"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actualPage=actualPage, customColumn=customColumn )


        varsPage        = self.generateHeader(CustomTitle=_('sellers').title())
        return render(request, 'admin/actor/sellersList.html', {'tabla': tabla,'varsPage':varsPage})

##ADMINISTRATOR##
class Administrator(Actor):
    varsPage = {
                'btnAdministratorsClass':'active',
                'nameCreateURL':'dashboard:actor-administrators-create',
                }

    @method_decorator(login_required)
    def showList(self,request):
        actualPage      = getActualPage(request)
        arg             = {"page": actualPage}
        ObjApi          = api()
        data            = ObjApi.get(slug='administrators/',arg=arg,request=request)

        customColumn    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-administrators-detail','key':'id'}}
                          }
        lastnamesTitle  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        header_tabla    = {lastnamesTitle: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("specialty"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actualPage=actualPage, customColumn=customColumn )


        varsPage        = self.generateHeader(CustomTitle=_('administrators').title())
        return render(request, 'admin/actor/administratorsList.html', {'tabla': tabla,'varsPage':varsPage})