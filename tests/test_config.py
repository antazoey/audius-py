from audius.config import Config
from audius.types import PlayerType


class TestConfig:
    def test_app_name_form_env(self, app_name_from_env):
        config = Config.from_env()
        assert config.app_name == app_name_from_env

    def test_host_from_env(self, host_from_env):
        config = Config.from_env()
        assert config.host == host_from_env

    def test_player_from_env(self, player_from_env):
        config = Config.from_env()
        assert config.player == PlayerType(player_from_env)
