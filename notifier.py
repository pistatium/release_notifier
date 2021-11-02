from abc import abstractmethod, ABCMeta


class Notifier(metaclass=ABCMeta):
    @abstractmethod
    def notify_success(self):
        pass

    @abstractmethod
    def notify_fail(self):
        pass
