from audius.client_factory import ClientFactory


class Audius:
    factory = ClientFactory()
    client = None

    def get_hosts(self):
        if self.client is not None:
            return self.client

        host_list = self.factory.get_hosts()
        return host_list


sdk = Audius()
