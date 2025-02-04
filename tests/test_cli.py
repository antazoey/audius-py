from subprocess import PIPE, run

import pytest

from audius.cli import hosts


@pytest.fixture
def run_cmd():
    class Result:
        def __init__(self, process_result):
            self.process_result = process_result

        @property
        def exit_code(self) -> int:
            return self.process_result.returncode

        @property
        def output(self) -> str:
            return self.process_result.stdout.decode("utf8")

    def fn(*args):
        cmd = ["audius", *args]
        process_result = run(cmd, stdout=PIPE, stderr=PIPE)
        return Result(process_result)

    return fn


def test_cli(run_cmd):
    result = run_cmd()
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "hosts" in result.output
    assert "List available hosts" in result.output


def test_app_name(run_cmd):
    result = run_cmd("config", "app-name")
    assert result.output == "audius-py\n"


def test_hosts(mocker, capsys):
    hosts_patch = mocker.patch("audius.cli.get_hosts")
    host_strings = ["http://host1.example.com", "https://host2.example.com"]

    def patch():
        yield from host_strings

    hosts_patch.side_effect = patch

    hosts()
    result = capsys.readouterr()
    assert result.out == "\n".join(host_strings) + "\n"
