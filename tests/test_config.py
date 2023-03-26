from audius.config import Config


class TestConfig:
    def test_app_name_form_env(self, app_name_from_env):
        config = Config.from_env()
        assert config.app_name == app_name_from_env

    def test_host_from_env(self, host_from_env):
        config = Config.from_env()
        assert config.host == host_from_env
