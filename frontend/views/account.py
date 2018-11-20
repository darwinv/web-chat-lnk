
from django.http import JsonResponse
from django.shortcuts import render
from api.connection import api

class Client:
    def status(self, request, pk):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='account_status/client/' + pk, token=token)
    
        month_api = resp['mounth']
        month = []
        for plan in month_api['plans']:
            month.append({"number":plan['query_quantity'], "text":plan['plan_name']})
            month.append({"number":plan['queries_used'], "text":"Consultas absueltas"})
            month.append({"number":plan['available_queries'], "text":"Consultas disponibles"})

        month.append({"number":month_api['match_acquired'], "text":"Match"})
        month.append({"number":month_api['match_absolved'], "text":"Match aceptados"})
        month.append({"number":month_api['match_declined'], "text":"Match declinados"})

        historic_api = resp['historic']
        historic = []
        historic.append({"number":historic_api['queries_acquired'], "text":"Consultas adquiridas"})
        historic.append({"number":historic_api['queries_made'], "text":"Consultas absueltas"})
        historic.append({"number":historic_api['queries_available'], "text":"Consultas disponibles"})

        if month and historic:
            return render(request, 'frontend/actors/client/account_status.html', {'month':month, 'historic':historic})
        else:
            return JsonResponse({})

class Specialist:
    def status(self, request, pk):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='account_status/specialist/' + pk, token=token)

        month_api = resp['mounth']
        month = []

        month.append({"number":month_api['queries_category_total'], "text":"Consultas recibidas"})
        month.append({"number":month_api['queries_category_absolved'], "text":"Consultas absueltas"})
        month.append({"number":month_api['queries_category_pending'], "text":"Consultas pendientes"})

        if resp['type_specialist'] == 'm':
            month.append({"number":month_api['queries_main_total'], "text":"Especialista principal"})
            month.append({"number":month_api['queries_main_absolved'], "text":"Principal absueltas"})
            month.append({"number":month_api['queries_main_pending'], "text":"Principal pendientes"})

            month.append({"number":month_api['queries_asociate_total'], "text":"Especialistas asociados"})
            month.append({"number":month_api['queries_asociate_absolved'], "text":"Asociados absueltas"})
            month.append({"number":month_api['queries_asociate_pending'], "text":"Asociados pendientes"})

        month.append({"number":month_api['match_total'], "text":"Match"})
        month.append({"number":month_api['match_accepted'], "text":"Match aceptados"})
        month.append({"number":month_api['match_declined'], "text":"Match declinados"})

        historic_api = resp['historic']
        historic = []
        historic.append({"number":historic_api['queries_main_absolved'], "text":"Consultas absueltas"})
        historic.append({"number":historic_api['match_accepted'], "text":"Match aceptados"})

        if resp:
            return render(request, 'frontend/actors/client/account_status.html', {'month':month, 'historic':historic})
        else:
            return JsonResponse({})

    def associates(self, request):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='specialists/associate/', token=token)

        associates = resp['results']
        count = resp['count']

        return render(request, 'frontend/actors/specialist/associate_list.html', {'associates':associates, 'count':count})

    def associate(self, request, pk):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='specialists/' + pk, token=token)

        data_user = resp
        name = data_user['first_name'] + ' ' + data_user['last_name']
        type_specialist = data_user['type_specialist']
        if type_specialist == 'a':
            type_specialist = 'Especialista asociado'
        elif type_specialist == 'm':
            type_specialist = 'Especialista principal'

        return render(request, 'frontend/actors/specialist/my_account.html', {
            'data_user':data_user, 'type_specialist':type_specialist, 'name':name
        })
