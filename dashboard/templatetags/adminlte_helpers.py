from hashlib import md5

from django import template
from django.conf import settings


from django.template import Library
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language

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
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    url_parts = resolve( path )

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
    finally:
        activate(cur_language)


    return "%s" % url