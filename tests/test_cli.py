import pytest
from click.testing import CliRunner

from audius.cli import audius


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return audius


def test_cli(runner, cli):
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0


def test_app_name(runner, cli):
    result = runner.invoke(cli, ["config", "app-name"])
    assert result.output == "audius-py\n"


def test_hosts(mocker, runner, cli):
    hosts_patch = mocker.patch("audius.cli.get_hosts")
    hosts = ["http://host1.example.com", "https://host2.example.com"]

    def patch():
        yield from hosts

    hosts_patch.side_effect = patch

    result = runner.invoke(cli, "hosts")
    assert result.output == "\n".join(hosts) + "\n"
