from abc import ABCMeta, abstractmethod


class IAskable(metaclass=ABCMeta):
    @abstractmethod
    def ask(self, message: str) -> str:
        pass