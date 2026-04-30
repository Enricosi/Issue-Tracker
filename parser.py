import argparse


def parse_args():
    """Parse CLI arguments for the Issue Tracker.

    Subcommands:
        list            List issues, optionally filtered by status (-s) or developer (-d).
        add_issue       Create a new issue with title, priority (1-3), and assigned username.
                        Accepts an optional possible cause (-p).
        delete_issue    Delete an issue by its numeric ID.
        change_status   Update the status of an issue (open | in_progress | closed).
        add_developer   Register a new developer by username and first name.
                        Last name is optional (-l).
        remove_developer  Remove a developer by their numeric ID.

    Returns:
        argparse.Namespace: Parsed arguments with 'command' set to the chosen subcommand.
    """
    parser = argparse.ArgumentParser(description='Issue Tracker CLI')

    subparsers = parser.add_subparsers(dest="command")

    list_issues_parser = subparsers.add_parser('list_issues')
    list_issues_parser.add_argument('-s', '--status', choices=['open', 'in_progress', 'closed'])
    list_issues_parser.add_argument('-u', '--username')

    add_issue_parser = subparsers.add_parser('add_issue')
    add_issue_parser.add_argument('title')
    add_issue_parser.add_argument('priority', type=int, choices=[1, 2, 3])
    add_issue_parser.add_argument('-u', '--username')
    add_issue_parser.add_argument('-p', '--posible_cause')

    delete_issue_parser = subparsers.add_parser('delete_issue')
    delete_issue_parser.add_argument('id', type=int)

    change_status_parser = subparsers.add_parser('change_status')
    change_status_parser.add_argument('id', type=int)
    change_status_parser.add_argument('new_status', choices=['open', 'in_progress', 'closed'])

    list_developer_parser = subparsers.add_parser('list_developers')

    add_developer_parser = subparsers.add_parser('add_developer')
    add_developer_parser.add_argument('username')
    add_developer_parser.add_argument('first_name')
    add_developer_parser.add_argument('-l', '--last_name')

    remove_developer_parser = subparsers.add_parser('remove_developer')
    remove_developer_parser.add_argument('username')

    reassing_issue_parser = subparsers.add_parser('reassing_issue')
    reassing_issue_parser.add_argument('id', type=int)
    reassing_issue_parser.add_argument('username')
    
    
    
    return parser.parse_args()