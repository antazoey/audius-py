import os
from contextlib import contextmanager

import pytest

from audius.config import AUDIUS_APP_NAME_ENV_VAR, AUDIUS_HOST_NAME_ENV_VAR, AUDIUS_PLAYER_ENV_VAR


@pytest.fixture
def app_name():
    return "test-audius-app-name"


@pytest.fixture
def host():
    return "https://audius.example.com"


@pytest.fixture
def player():
    return "VLC"


@contextmanager
def temp_set_env(key: str, value: str):
    existing = os.environ.get(key)
    try:
        os.environ[key] = value
        yield
    finally:
        if existing:
            os.environ[key] = existing


@pytest.fixture
def app_name_from_env(app_name):
    with temp_set_env(AUDIUS_APP_NAME_ENV_VAR, app_name):
        yield app_name


@pytest.fixture
def host_from_env(host):
    with temp_set_env(AUDIUS_HOST_NAME_ENV_VAR, host):
        yield host


@pytest.fixture
def player_from_env(player):
    with temp_set_env(AUDIUS_PLAYER_ENV_VAR, player):
        yield player
