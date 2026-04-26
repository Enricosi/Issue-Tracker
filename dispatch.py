from commands_issues import *
from commands_developer import *

def dispatch(args, conn):
    """Route parsed CLI arguments to the corresponding command handler.

    Looks up args.command in a dispatch table and calls the matching function,
    passing the full args namespace so each handler can read its own arguments.

    Args:
        args (argparse.Namespace): Parsed arguments returned by parse_args(),
            must include a 'command' attribute.

    Returns:
        Any: Whatever the invoked command handler returns.

    Raises:
        RuntimeError: If args.command does not match any known command.
    """
    handlers = {
        'list' : cmd_list,
        'add_issue' : cmd_add_issue,
        'delete_issue' : cmd_delete_issue,
        'change_status' : cmd_change_status,
        'list_developers' : cmd_list_developers,
        'add_developer' : cmd_add_developer,
        'remove_developer' : cmd_remove_developer
    }

    cmd = args.command

    fn  = handlers.get(cmd)

    if fn is None:
        raise RuntimeError('Comando desconocido')
    
    return fn(args, conn)