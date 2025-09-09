from abc import ABC, abstractmethod

class AuthProvider(ABC):
    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def _get_token(self):
        pass

    @abstractmethod
    def _get_tenant_dns(self):
        pass