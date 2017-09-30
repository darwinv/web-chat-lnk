from django import template
from api.config import template


@register.simple_tag(takes_context=True)
def avatar_url(context):
    # TODO: Make behaviour configurable
    user = context['request'].user
    return 'https://www.gravatar.com/avatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.email.encode('utf-8')).hexdigest() if user.is_authenticated() else '',
        size=size or '',
    )
