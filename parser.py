import argparse


def parse_args():
    """Parse CLI arguments for the Issue Tracker.

    Subcommands:
        list_issues       List issues. Optional: -s/--status, -u/--username.
        add_issue         Create an issue with title and priority (1-3).
                          Optional: -u/--username (assign developer), -p/--posible_cause.
        delete_issue      Delete a closed issue by ID.
        change_status     Change issue status (open | in_progress | closed) by ID.
        list_developers   List all developers with their active issue count.
        add_developer     Register a developer with username and first_name.
                          Optional: -l/--last_name.
        remove_developer  Remove a developer by username.
        reassing_issue    Reassign an issue (by ID) to a different developer (by username).

    Returns:
        argparse.Namespace: Parsed arguments with 'command' set to the chosen subcommand.
    """
    parser = argparse.ArgumentParser(description='Issue Tracker CLI')

    subparsers = parser.add_subparsers(dest="command")

    list_issues_parser = subparsers.add_parser('list_issues', help="Muestra la lista de todos los issues en la base de datos que coinciden con los filtros aplicados. Opcional.")
    list_issues_parser.add_argument('-s', '--status', choices=['open', 'in_progress', 'closed'], help="Filtra los issue segun el estado indicado.")
    list_issues_parser.add_argument('-u', '--username', help="Filtra los issue del desarrollador indicado y se puede combinar con --status para mostrar solo los que tienen ese estado. Opcional.")

    add_issue_parser = subparsers.add_parser('add_issue', help="Crea un nuevo issue en la base de datos.")
    add_issue_parser.add_argument('title', help="Titulo del issue.")
    add_issue_parser.add_argument('priority', type=int, choices=[1, 2, 3], help="Indica la prioridad del issue siendo 3 la maxima.")
    add_issue_parser.add_argument('-u', '--username', help="Desarrollador al que sera asignado el issue. Opcional.")
    add_issue_parser.add_argument('-p', '--posible_cause', help="Posible causa del issue. Opcional.")

    delete_issue_parser = subparsers.add_parser('delete_issue', help="Elimina el issue de la base de datos.")
    delete_issue_parser.add_argument('id', type=int, help="ID del issue.")

    change_status_parser = subparsers.add_parser('change_status', help="Cambia el estado del issue indicado.")
    change_status_parser.add_argument('id', type=int, help="ID del issue.")
    change_status_parser.add_argument('new_status', choices=['open', 'in_progress', 'closed'], help="Estatus nuevo del issue. (open, in_progress, closed)")

    list_developer_parser = subparsers.add_parser('list_developers', help="Muestra la lista de todos los desarrolladores en la base de datos.")

    add_developer_parser = subparsers.add_parser('add_developer', help="Agrega un nuvo desarrollador a la base de datos.")
    add_developer_parser.add_argument('username', help="Username del nuevo desarrollador.")
    add_developer_parser.add_argument('first_name', help="Nombre del nuevo desarrollador.")
    add_developer_parser.add_argument('-l', '--last_name', help="Apellido del nuevo desarrollador. Opcional.")

    remove_developer_parser = subparsers.add_parser('remove_developer', help="Elimina un desarrollador de la base de datos.")
    remove_developer_parser.add_argument('username', help="Username del desarrollador.")

    reassing_issue_parser = subparsers.add_parser('reassing_issue', help="Reasigna un issue a un desarrollador o cambia el desarrollador asignado a este.")
    reassing_issue_parser.add_argument('id', type=int, help="ID del issue.")
    reassing_issue_parser.add_argument('username', help="Username del desarrollador.")
    
    
    
    return parser.parse_args()