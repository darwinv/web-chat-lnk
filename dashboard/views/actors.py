from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


from api.connection import api

from dashboard.json2table import convert,getActualPage
from dashboard.forms import SpecialistForm

class Actor:
    logo_content_header    = "fa fa-users"
    title_content_header   = "{} - ".format(_("actors").title())

    def generateHeader(self,custom_title=None):
        if custom_title:
            title = self.title_content_header + custom_title
        else:
            title = self.title_content_header

        header = {'icon':self.logo_content_header,'title':title}
        return {**header, **self.vars_page}


class Specialist(Actor):
    vars_page = {
                'btn_specialists_class':'active',
                'name_create_URL':'dashboard:actor-specialists-create',
                }

    @method_decorator(login_required)
    def list(self,request):
        ObjApi          = api()
        filters         = {}
        actual_page     = getActualPage(request)
        arg             = {"page": actual_page}

        # Filtro de especialista principal
        if 'mainSpecialist' in request.GET:
            mainSpecialist      =  request.GET['mainSpecialist']
            arg.update({"mainSpecialist": mainSpecialist})
            dataMainSpecilist   = ObjApi.get(slug='specialists/'+mainSpecialist,token=request.session['token'])
            filters.update({'mainSpecialist':dataMainSpecilist})


        # Traer data para el listado
        data            = ObjApi.get(slug='specialists/',arg=arg,token=request.session['token'])

        # Definimos columnas adicionales/personalizadas
        custom_column    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-specialists-detail','key':'id'}},
                            "delete": {'type':'delete','data':{'class':'deleteSpecialist','key':'id'}}
                          }
        
        # Coloca los nombres de las cabeceras y a que columna van asociada, customColum tendra prioriedad
        lastnames_title  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        header_tabla    = {lastnames_title: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("specialty"): "",_("detail"): "detail",_("delete"): "delete"}

        tabla           = convert(data, header=header_tabla,actual_page=actual_page, custom_column=custom_column )

        
        title_page      = _('specialists').title()
        vars_page       = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/specialistsList.html', {'tabla': tabla,'vars_page':vars_page,'filters':filters})


    @method_decorator(login_required)
    def detail(self,request,specialist_id):
        ObjApi = api()
        data   = ObjApi.get(slug='specialists/'+specialist_id,token=request.session['token'])

        # Si la data del usuario no es valida
        if type(data) is not dict or 'id' not in data:
            raise Http404()


        if type(data) is dict and 'type_specialist' in data:
            type_specialist = data['type_specialist']
        else:
            type_specialist = ''

        title_page     = "{} {} - {}".format(_('specialist').title(),_(type_specialist),_('detail').title())
        vars_page      = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/specialistsDetail.html',{'data': data,'vars_page':vars_page})


    @method_decorator(login_required)
    def create(self,request):
        ObjApi      = api()

        if request.method == 'POST':
            form = SpecialistForm(data=request.POST)            
            if form.is_valid():
                result = ObjApi.post(slug='specilist/',token=request.session['token'])
                return HttpResponseRedirect(reverse('dashboard:actor-specialists-list'))

        else:
            categories  = ObjApi.get(slug='categories/',token=request.session['token'])
            departments = ObjApi.get(slug='departments/',token=request.session['token'])
            form        = SpecialistForm(categories=categories['list'],departments=departments['list'])
                
        title_page     = _('create specialist').title()
        vars_page      = self.generateHeader(custom_title=title_page)

        return render(request, 'admin/actor/specialistsForm.html', {'vars_page':vars_page,'form':form})



    @method_decorator(login_required)
    def edit(self,request,specialist_id):
        ObjApi      = api()

        if request.method == 'POST':
            form = SpecialistForm(data=request.POST)
            # check whether it's valid:
            if form.is_valid():
                result = ObjApi.put(slug='specilist/'+specialist_id,token=request.session['token'])
                return HttpResponseRedirect(reverse('dashboard:actor-specialists-list'))

        else:
            specilist   = ObjApi.get(slug='specialists/'+specialist_id,token=request.session['token'])
            categories  = ObjApi.get(slug='categories/',token=request.session['token'])
            departments = ObjApi.get(slug='departments/',token=request.session['token'])

            # Si el usuario tiene department, traemos provincia
            if 'department' in specilist:
                arg = {'department':specilist['department']}
                provinces   = ObjApi.get(slug='provinces/',request=request,arg=arg)
            else:
                provinces   = {'list':None}

            # Si el usuario tiene province, traemos distritos
            if 'province' in specilist:
                arg = {'province':specilist['province']}
                districts   = ObjApi.get(slug='districts/',request=request,arg=arg)
            else:
                districts   = {'list':None}

            form        = SpecialistForm(categories=categories['list'],departments=departments['list'],provinces=provinces['list'],districts=districts['list'],initial=specilist)

        title_page     = _('edit specialist').title()
        vars_page      = self.generateHeader(custom_title=title_page)
        return render(request, 'admin/actor/specialistsForm.html', {'vars_page':vars_page,'form':form})

    
    @method_decorator(login_required)
    def delete(self,request):
        if request.method == 'POST':
            specialist_id   = request.POST['specialist_id']
            ObjApi          = api()
            result          = ObjApi.delete(slug='specialists/'+specialist_id,token=request.session['token'])

            return JsonResponse({'result': result})

        return JsonResponse({})



class Client(Actor):
    vars_page = {
                'btnClientsClass':'active',
                'nameCreateURL':'dashboard:actor-clients-create',
                }

    @method_decorator(login_required)
    def list(self,request):
        actual_page      = getActualPage(request)
        arg             = {"page": actual_page}
        ObjApi          = api()
        data            = ObjApi.get(slug='clients/',arg=arg,token=request.session['token'])
        

        custom_column    = {
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-clients-detail','key':'id'}}
                          }
        lastnames_title  = "{}/{}".format(_("names"),_("business name"))
        header_tabla    = {lastnames_title: "bussiness_name", _("alias"): "nick", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("identification document"): "document_number",_("RUC"): "ruc",_("category"): "",_("consultas"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actual_page=actual_page, custom_column=custom_column )


        vars_page        = self.generateHeader(custom_title=_('clients').title())
        return render(request, 'admin/actor/clientsList.html', {'tabla': tabla,'vars_page':vars_page})



class Seller(Actor):
    vars_page = {
                'btnSellersClass':'active',
                'nameCreateURL':'dashboard:actor-sellers-create',
                }

    @method_decorator(login_required)
    def list(self,request):
        actual_page      = getActualPage(request)
        arg             = {"page": actual_page}
        ObjApi          = api()
        data            = ObjApi.get(slug='sellers/',arg=arg,token=request.session['token'])

        custom_column    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-sellers-detail','key':'id'}}
                          }
        lastnames_title  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        viewCient       = "{} {}".format(_("view"),_("clients"))
        header_tabla    = {lastnames_title: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc",_("viewCient"): "", _("ubigeo"): "",
                           _("fee"): "",_("advance"): "",_("number of plans sold"): "",_("number of queries"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actual_page=actual_page, custom_column=custom_column )


        vars_page        = self.generateHeader(custom_title=_('sellers').title())
        return render(request, 'admin/actor/sellersList.html', {'tabla': tabla,'vars_page':vars_page})


class Administrator(Actor):
    vars_page = {
                'btnAdministratorsClass':'active',
                'nameCreateURL':'dashboard:actor-administrators-create',
                }

    @method_decorator(login_required)
    def list(self,request):
        actual_page      = getActualPage(request)
        arg             = {"page": actual_page}
        ObjApi          = api()
        data            = ObjApi.get(slug='administrators/',arg=arg,token=request.session['token'])

        custom_column    = {
                            "last_name": {'type':'concat','data':{'username', 'last_name'}},
                            "detail": {'type':'detail','data':{'href':'dashboard:actor-administrators-detail','key':'id'}}
                          }
        lastnames_title  = "{} {} {}".format(_("surnames"),_("and"),_("names"))
        header_tabla    = {lastnames_title: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "",
                           _("specialty"): "",_("detail"): "detail"}
        tabla           = convert(data, header=header_tabla,actual_page=actual_page, custom_column=custom_column )


        vars_page        = self.generateHeader(custom_title=_('administrators').title())
        return render(request, 'admin/actor/administratorsList.html', {'tabla': tabla,'vars_page':vars_page})