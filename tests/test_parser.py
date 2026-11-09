import sys

import pytest

from parser import parse_args


def parse(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["issue_tracker.py", *argv])
    return parse_args()


def test_add_issue_with_optional_fields(monkeypatch):
    args = parse(monkeypatch, "add_issue", "Login fails", "2", "-u", "john", "-p", "Expired token")
    assert args.command == "add_issue"
    assert args.priority == 2
    assert args.username == "john"
    assert args.posible_cause == "Expired token"


def test_priority_out_of_range_is_rejected(monkeypatch):
    with pytest.raises(SystemExit):
        parse(monkeypatch, "add_issue", "Login fails", "4")


def test_invalid_status_is_rejected(monkeypatch):
    with pytest.raises(SystemExit):
        parse(monkeypatch, "change_status", "1", "done")


def test_reassign_issue(monkeypatch):
    args = parse(monkeypatch, "reassign_issue", "5", "maria")
    assert (args.command, args.id, args.username) == ("reassign_issue", 5, "maria")
