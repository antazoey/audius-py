from audius.sdk import Audius


class TestAudius:
    def test_app_name_form_env(self, app_name_from_env):
        sdk = Audius()
        assert sdk.config.app_name == app_name_from_env

    def test_host_from_env(self, host_from_env):
        sdk = Audius()
        assert sdk.config.host == host_from_env
