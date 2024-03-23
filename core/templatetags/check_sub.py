from django import template
from ..models import Creator

register = template.Library()

@register.filter()
def is_subscribed(creator_id, user):
    creator = Creator.objects.filter(pk=creator_id).first()
    if creator is not None:
        if creator.subscribers.filter(pk=user.pk).exists(): 
            return True
        else:
            return False
    return False
    

  