from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def select(self, table, columns, conditions):
        pass

    @abstractmethod
    def insert(self, table, data):
        pass

    @abstractmethod
    def update(self, table, data, conditions):
        pass

    @abstractmethod
    def delete(self, table, conditions):
        pass
