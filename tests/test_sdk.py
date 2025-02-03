from audius import Audius
from audius.types import PlayerType


class TestAudius:
    def test_app_name_form_env(self, app_name_from_env):
        sdk = Audius()
        assert sdk.app_name == app_name_from_env
        assert sdk.config.app_name == app_name_from_env

    def test_app_name_from_argument(self):
        name = "TestAppNameFromArgument"
        sdk = Audius(name)
        assert sdk.app_name == name
        assert sdk.config.app_name == name

    def test_host_from_env(self, host_from_env):
        sdk = Audius()
        assert sdk.config.host == host_from_env

    def test_player_from_env(self, player_from_env):
        sdk = Audius()
        assert sdk.config.player == PlayerType(player_from_env)
