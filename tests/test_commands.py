from argparse import Namespace

import pymysql
import pytest

from commands_developer import cmd_add_developer, cmd_remove_developer
from commands_issues import cmd_add_issue, cmd_change_status, cmd_delete_issue, cmd_reassign_issue
from dispatch import dispatch
from exceptions import IssueTrackerError


def test_unknown_command_raises(fake_conn):
    with pytest.raises(RuntimeError):
        dispatch(Namespace(command="nope"), fake_conn())


def test_add_issue_with_unknown_developer_does_not_insert(fake_conn):
    conn = fake_conn(results=[None])  # developer lookup finds nothing
    args = Namespace(title="Bug", priority=1, username="ghost", posible_cause=None)
    with pytest.raises(IssueTrackerError):
        cmd_add_issue(args, conn)
    assert conn.commits == 0
    assert not any(sql.startswith("INSERT") for sql, _ in conn.executed)


def test_add_issue_assigns_developer(fake_conn):
    conn = fake_conn(results=[(7,)])
    args = Namespace(title="Bug", priority=3, username="john", posible_cause="Cache")
    cmd_add_issue(args, conn)
    sql, values = conn.executed[-1]
    assert sql.startswith("INSERT INTO issue")
    assert values == ("Bug", "Cache", 3, 7)
    assert conn.commits == 1


def test_open_issue_cannot_be_deleted(fake_conn):
    conn = fake_conn(results=[(1,), None])  # exists, but not closed
    with pytest.raises(IssueTrackerError):
        cmd_delete_issue(Namespace(id=1), conn)
    assert conn.commits == 0


def test_change_to_same_status_raises(fake_conn):
    conn = fake_conn(results=[(1,), ("open",)])
    with pytest.raises(IssueTrackerError):
        cmd_change_status(Namespace(id=1, new_status="open"), conn)


def test_closing_an_issue_sets_close_date(fake_conn):
    conn = fake_conn(results=[(1,), ("in_progress",)])
    cmd_change_status(Namespace(id=1, new_status="closed"), conn)
    _, values = conn.executed[-1]
    new_status, close_date, issue_id = values
    assert new_status == "closed"
    assert close_date is not None
    assert issue_id == 1


def test_reassign_to_same_developer_raises(fake_conn):
    conn = fake_conn(results=[(1, 7), (7, "john")])
    with pytest.raises(IssueTrackerError):
        cmd_reassign_issue(Namespace(id=1, username="john"), conn)


def test_developer_with_issues_cannot_be_removed(fake_conn):
    conn = fake_conn(results=[(7,), (2,)])
    with pytest.raises(IssueTrackerError):
        cmd_remove_developer(Namespace(username="john"), conn)
    assert conn.commits == 0


def test_duplicate_username_rolls_back(fake_conn):
    conn = fake_conn(raise_on_execute=pymysql.err.IntegrityError())
    args = Namespace(username="john", first_name="john", last_name=None)
    with pytest.raises(IssueTrackerError):
        cmd_add_developer(args, conn)
    assert conn.rollbacks == 1


def test_list_issues_without_filters_prints_all(fake_conn, capsys):
    from commands_issues import cmd_list_issues

    row = (1, "Bug", None, "2026-01-01 10:00:00", None, "open", 2, None)
    conn = fake_conn(results=[[row]])
    cmd_list_issues(Namespace(status=None, username=None), conn)
    assert "ID: 1 | Title: Bug" in capsys.readouterr().out


def test_list_issues_on_empty_table_raises(fake_conn):
    from commands_issues import cmd_list_issues

    with pytest.raises(IssueTrackerError):
        cmd_list_issues(Namespace(status=None, username=None), fake_conn(results=[[]]))
