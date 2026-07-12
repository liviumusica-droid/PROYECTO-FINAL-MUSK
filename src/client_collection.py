from src.client import Client

class ClientCollection:
    def __init__(self, clients_list: list[Client]):
        self.clients = clients_list

    def get_client_by_id(self, client_id: int) -> Client | None:
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def clients_by_country(self, country: str) -> list[Client]:
        return [client for client in self.clients if client.country.lower() == country.lower()]