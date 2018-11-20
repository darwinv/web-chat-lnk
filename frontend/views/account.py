
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
            month.append({"number":plan['queries_used'], "text":"Absolved queries"})
            month.append({"number":plan['available_queries'], "text":"Available queries"})

        month.append({"number":month_api['match_acquired'], "text":"Match"})
        month.append({"number":month_api['match_absolved'], "text":"Match accepted"})
        month.append({"number":month_api['match_declined'], "text":"Match declined"})

        historic_api = resp['historic']
        historic = []
        historic.append({"number":historic_api['queries_acquired'], "text":"Acquired queries"})
        historic.append({"number":historic_api['queries_made'], "text":"Absolved queries"})
        historic.append({"number":historic_api['queries_available'], "text":"Available queries"})

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

        month.append({"number":month_api['queries_category_total'], "text":"Received queries"})
        month.append({"number":month_api['queries_category_absolved'], "text":"Absolved queries"})
        month.append({"number":month_api['queries_category_pending'], "text":"Pending queries"})

        if resp['type_specialist'] == 'm':
            month.append({"number":month_api['queries_main_total'], "text":"Main specialist"})
            month.append({"number":month_api['queries_main_absolved'], "text":"Absolved main"})
            month.append({"number":month_api['queries_main_pending'], "text":"Pending main"})

            month.append({"number":month_api['queries_asociate_total'], "text":"Associated specialists"})
            month.append({"number":month_api['queries_asociate_absolved'], "text":"Absolved associates"})
            month.append({"number":month_api['queries_asociate_pending'], "text":"Pending associates"})

        month.append({"number":month_api['match_total'], "text":"Match"})
        month.append({"number":month_api['match_accepted'], "text":"Match accepted"})
        month.append({"number":month_api['match_declined'], "text":"Match declines"})

        historic_api = resp['historic']
        historic = []
        historic.append({"number":historic_api['queries_main_absolved'], "text":"Absolved queries"})
        historic.append({"number":historic_api['match_accepted'], "text":"Match accepted"})

        if resp:
            return render(request, 'frontend/actors/client/account_status.html', {'month':month, 'historic':historic})
        else:
            return JsonResponse({})
