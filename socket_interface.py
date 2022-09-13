from abc import ABC, abstractmethod


class SocketInterface(ABC):

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def send(self, msg: bytes) -> None:
        raise NotImplementedError
