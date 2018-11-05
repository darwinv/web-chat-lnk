from hashlib import md5

from django import template
from django.conf import settings

from django.template import Library
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language
from django.utils.translation import ugettext_lazy as _
from dashboard.tools import ToolsBackend as Tools
import re
register = template.Library()


@register.simple_tag()
def logout_url():
    return getattr(settings, 'LOGOUT_URL', '/logout/')


@register.simple_tag(takes_context=True)
def avatar_url(context, size=None):
    # TODO: Make behaviour configurable
    user = context['request'].user
    return 'https://www.gravatar.com/avatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.email.encode('utf-8')).hexdigest() if user.is_authenticated() else '',
        size=size or '',
    )

@register.filter()
def upfirstletter(value):
    first = value[0] if len(value) > 0 else ''
    remaining = value[1:] if len(value) > 1 else ''
    return first.upper() + remaining


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, default_arg=True, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}

    :param lang: codigo de idioma
    :param default_arg: permite reenviar valores GET
    :return: string con la ruta para cambiar el lenguaje
    """
    path = context['request'].path

    url_parts = resolve(path)

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)

    finally:
        activate(cur_language)

    if default_arg:
        get_request = context['request'].GET
        get_values = ""
        for key in get_request:
            get_values = "{name}={value}".format(name=key, value=get_request[key])

        if get_values:
            url = "{}?{get_values}".format(url, get_values=get_values)

    return "%s" % url

@register.filter()
def datetime_format_to_view(date):
    """date: str 2018-02-08 14:28:25+00:00"""
    if date:
        tools = Tools()
        return tools.datetime_format_to_view(date=date)
    else:
        return date

@register.filter()
def bolean_translate(bolean):
    """bolean: bolean"""
    if bolean:
        return _("yes").title()
    else:
        return _("no").title()

@register.simple_tag()
def is_mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False