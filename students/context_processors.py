from .util import get_groups

def get_groups_proc(request):
    """
    GROUPS - are made from uppercase letter for convenience
    in templates you can see
    that this variable came from context processor
    """
    return {'GROUPS': get_groups(request)}
