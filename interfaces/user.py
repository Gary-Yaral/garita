from abc import ABC, abstractmethod

class UserAbstract(ABC):
    @abstractmethod
    def find_user(self, username):
        pass

    """ @abstractmethod
    def get_user(self, id):
        pass
    
    @abstractmethod
    def get_all(self, id):
        pass

    @abstractmethod
    def insert(self, id):
        pass
    
    @abstractmethod
    def update(self, id, nuevos_datos):
        pass

    @abstractmethod
    def delete(self, id):
        pass """
