from commands_issues import *
from commands_developer import *

def dispatch(args):

    handlers = {
        'list' : cmd_list,
        'add_issue' : cmd_add_issue,
        'delete_issue' : cmd_delete_issue,
        'change_status' : cmd_change_status,
        'add_developer' : cmd_add_developer,
        'remove_developer' : cmd_remove_developer
    }

    cmd = args.command

    fn  = handlers.get(cmd)

    if fn is None:
        raise RuntimeError('Comando desconocido')
    
    return fn(args)