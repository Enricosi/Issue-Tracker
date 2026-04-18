import argparse
def parse_args():
    parser = argparse.ArgumentParser(description='Issue Tracker CLI')

    subparsers = parser.add_subparsers(dest="command")

    # PARSER DEL CMD LIST:
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-s', '--status', choices=['open', 'in_progress', 'closed'])
    list_parser.add_argument('-d', '--dev')

    # PARSER DEL CMD ADD_ISSUE:
    add_issue_parser = subparsers.add_parser('add_issue')
    add_issue_parser.add_argument('title')
    add_issue_parser.add_argument('priority', type=int, choices=[1, 2, 3])
    add_issue_parser.add_argument('username')
    add_issue_parser.add_argument('-p', '--posible_cause')

    # PARSER DE DELETE:
    delete_issue_parser = subparsers.add_parser('delete_issue')
    delete_issue_parser.add_argument('id', type=int)

    # CHANGE_STATUS_PARSER:
    change_status_parser = subparsers.add_parser('change_status')
    change_status_parser.add_argument('id', type=int)
    change_status_parser.add_argument('new_status', choices=['open', 'in_progress', 'closed'])

    # ADD_DEVELOPER_PARSER:
    add_developer_parser = subparsers.add_parser('add_developer')
    add_developer_parser.add_argument('username')
    add_developer_parser.add_argument('first_name')
    add_developer_parser.add_argument('-l', '--last_name')

    # REMOVE_DEVELOPER_PARSER:
    remove_developer_parser = subparsers.add_parser('remove_developer')
    remove_developer_parser.add_argument('id', type=int)

    return parser.parse_args()