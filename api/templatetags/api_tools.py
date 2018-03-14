from django import template

from api.config import API_URL, API_HEADERS
from django.http import JsonResponse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_api_url(context):
    return API_URL


@register.simple_tag(takes_context=True)
def get_api_header(context):
    return API_HEADERS

# 
# @register.simple_tag(takes_context=True)
# def get_api_url(context):
#     return API_URL
