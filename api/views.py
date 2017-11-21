from django.shortcuts import render
from api.models import Category, Department, Province, District
from django.http import JsonResponse, HttpResponse
from django.core import serializers
# Create your views here.
def provinces_by_deparment(request):
    if request.GET['department']:
        department = request.GET['department']
        provinces = Province.objects.filter(department_id=department)
        return JsonResponse(serializers.serialize('json', provinces), safe=False)

    return JsonResponse({})



def districts_by_province(request):
    if request.GET['province']:
        province = request.GET['province']
        provinces = District.objects.filter(province_id=province)
        return JsonResponse(serializers.serialize('json', provinces), safe=False)

    return JsonResponse({})