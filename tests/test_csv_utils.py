import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import csv_utils  # noqa: E402


@pytest.fixture
def chat_file(tmp_path):
    return str(tmp_path / "chats.csv")


def make_chat(chat_id=1, username="alex"):
    return {
        "id": chat_id,
        "type": "private",
        "username": username,
        "first_name": "Alex",
        "last_name": "Messer",
    }


def test_chat_object_parses_csv_row():
    obj = csv_utils.ChatObject(["42", "private", "alex", "Alex", "Messer", "2026-11-14 13:00:00"])

    assert obj.id == 42
    assert obj.type == "private"
    assert obj.username == "alex"
    assert obj.first_name == "Alex"
    assert obj.last_name == "Messer"
    assert obj.first_contact == "2026-11-14 13:00:00"


def test_writer_creates_missing_file(chat_file):
    assert not os.path.exists(chat_file)

    writer = csv_utils.Writer(file=chat_file)

    assert os.path.isfile(chat_file)
    assert writer.entries == []


def test_writer_keeps_existing_file(chat_file):
    with open(chat_file, "w") as f:
        f.write("1;private;alex;Alex;Messer;2026-11-14 13:00:00;\n")

    writer = csv_utils.Writer(file=chat_file)

    assert len(writer.entries) == 1
    assert writer.entries[0].id == 1


def test_add_creates_entry_and_persists_it(chat_file):
    writer = csv_utils.Writer(file=chat_file)

    new = writer.add(make_chat(chat_id=7))

    assert new.id == 7
    assert len(writer.entries) == 1
    with open(chat_file) as f:
        content = f.read()
    assert content.startswith("7;private;alex;Alex;Messer;")
    assert content.endswith(";\n")


def test_add_returns_existing_entry_without_duplicate(chat_file):
    writer = csv_utils.Writer(file=chat_file)
    first = writer.add(make_chat(chat_id=7))

    second = writer.add(make_chat(chat_id=7))

    assert second is first
    assert len(writer.entries) == 1


def test_read_roundtrip_after_write(chat_file):
    writer = csv_utils.Writer(file=chat_file)
    writer.add(make_chat(chat_id=1, username="one"))
    writer.add(make_chat(chat_id=2, username="two"))

    reloaded = csv_utils.Writer(file=chat_file)

    assert [c.id for c in reloaded.entries] == [1, 2]
    assert [c.username for c in reloaded.entries] == ["one", "two"]


def test_search_id_returns_matches(chat_file):
    writer = csv_utils.Writer(file=chat_file)
    writer.add(make_chat(chat_id=1))
    writer.add(make_chat(chat_id=2))

    assert [c.id for c in writer.search_id(2)] == [2]
    assert writer.search_id(99) == []


def test_write_serializes_all_entries(chat_file):
    writer = csv_utils.Writer(file=chat_file)
    writer.entries = [csv_utils.ChatObject(["3", "group", "g", "G", "", "2026-01-01 00:00:00"])]

    writer.write()

    with open(chat_file) as f:
        assert f.read() == "3;group;g;G;;2026-01-01 00:00:00;\n"
