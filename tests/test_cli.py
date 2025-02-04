from subprocess import PIPE, run

import pytest


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


def test_hosts(mocker, runner, cli):
    hosts_patch = mocker.patch("audius.cli.get_hosts")
    hosts = ["http://host1.example.com", "https://host2.example.com"]

    def patch():
        yield from hosts

    hosts_patch.side_effect = patch

    result = runner.invoke(cli, "hosts")
    assert result.output == "\n".join(hosts) + "\n"
