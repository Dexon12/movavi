from abc import ABC, abstractmethod


class ParseByRequests(ABC):
    def __init__(self, email, proxy, **kwargs):
        self.email = email
        self.proxy = proxy
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def checker(self):
        raise Exception("[Base Class]: Implement 'checker' method, please")
    