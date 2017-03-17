from .util import get_groups

def get_groups_proc(request):
    return {'GROUPS': get_groups(request)}
