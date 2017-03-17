
from .models import Group

def get_groups(request):
    current_group = get_current_group(request)
    
    groups = []
    for group in Group.objects.order_by('title'):
        groups.append({
            'id':group.id,
            'title': group.title,
            'leader': group.leader and '%s %s' % (group.leader.first_name, group.leader.last_name) or None,
            'selected': current_group and current_group.id == group.id and True or False,
        })
    #import pdb; pdb.set_trace()

    return groups


def get_current_group(request):
    current_group = request.COOKIES.get('current_group')

    if current_group:
        try:
            group = Group.objects.get(pk=int(current_group))
        except Group.DoesNotExist:
            return None
    else:
        group = None

    return group
