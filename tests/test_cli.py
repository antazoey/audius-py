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
